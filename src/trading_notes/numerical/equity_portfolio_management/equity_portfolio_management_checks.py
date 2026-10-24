"""Worked numbers of equity portfolio management: indexing, active strategies, risk and capacity."""

import math
import sys
from typing import Final, cast

import numpy as np
import scipy
from numpy.typing import NDArray
from scipy.optimize import minimize

from trading_notes.numerical.equity_portfolio_management.equity_universe import (
    N,
    S,
    Universe,
    active_share,
)
from trading_notes.numerical.records import Record
from trading_notes.numerical.report import CheckReport, print_versions
from trading_notes.numerical.tolerance import close

type Floats = NDArray[np.float64]
type Ints = NDArray[np.int64]
type Indices = NDArray[np.intp]

SEED: Final = 20261019


class SlsqpFit(Record):
    """The parts of an SLSQP result that part 7 reads.

    Attributes:
        x: The long weights followed by the short weights.
        success: Whether the optimiser reported success.
    """

    x: Floats
    success: bool


def check_roles(report: CheckReport) -> None:
    """Part 1: income and costs of an index and an active mandate, and activist returns."""
    print("== part 1: roles, income and costs, and the active spectrum")
    div, lend_idx, lend_act = 0.018, 0.0005, 0.0002
    fee_idx, fee_act = 0.0004, 0.0065
    turn_idx, turn_act, cost_one_way = 0.05, 0.80, 0.0020
    net_idx = div + lend_idx - fee_idx - 2 * turn_idx * cost_one_way
    net_act = div + lend_act - fee_act - 2 * turn_act * cost_one_way
    report.ok(
        "income less costs on top of price return: index +1.79% (dividends 1.80, lending 0.05,"
        " fee 0.04, trading 0.02); active +0.85% (lending 0.02, fee 0.65, trading 0.32 at 80%"
        " turnover): the active manager starts 0.94% behind",
        abs(net_idx - 0.0179) < 1e-12
        and abs(net_act - 0.0085) < 1e-12
        and abs(net_idx - net_act - 0.0094) < 1e-12,
    )
    report.ok(
        "Brav et al. (2008): an activist stake announced by Schedule 13D earns 7-8% abnormal"
        " return over (-20, +20) days; on a 5% position that is 0.35-0.40% of the portfolio",
        close(0.05 * 0.07, 0.0035, 1e-12) and close(0.05 * 0.08, 0.004, 1e-12),
    )


def check_indexing(report: CheckReport, u: Universe, rng: np.random.Generator) -> Floats:
    """Part 2: cap-weighted, equal-weighted and value-tilted indexes; return the value tilt."""
    print("== part 2: cap-weighted against factor-based indexing")
    mcap, value, w_cap = u.mcap, u.value, u.w_cap
    w_eq = np.full(N, 1 / N)
    w_val = w_cap * np.exp(0.5 * value)
    w_val /= w_val.sum()
    ret = (
        rng.multivariate_normal(np.zeros(S + 2), u.F) @ u.B.T + rng.standard_normal(N) * u.idio
    )  # one year of returns
    value_new = 0.8 * value + 0.6 * rng.standard_normal(N)  # value scores a year later

    def target_after(scheme: str) -> Floats:
        if scheme == "cap":
            nc = mcap * (1 + ret)
            w_c: Floats = nc / nc.sum()
            return w_c
        if scheme == "eq":
            return w_eq
        nv = mcap * (1 + ret) * np.exp(0.5 * value_new)
        w_v: Floats = nv / nv.sum()
        return w_v

    turn = {}
    for scheme, w in (("cap", w_cap), ("eq", w_eq), ("val", w_val)):
        drift = w * (1 + ret)
        drift /= drift.sum()
        turn[scheme] = 0.5 * np.abs(target_after(scheme) - drift).sum()
    report.ok(
        "rebalancing turnover after a year: cap-weighted 0% (self-rebalancing); equal weight and"
        " the value tilt must trade back to target as prices and value scores change",
        turn["cap"] < 1e-12 and turn["eq"] > 0.05 and turn["val"] > 0.05,
        " ".join(f"{k} {v:.2%}" for k, v in turn.items()),
    )
    eff_n = {k: 1 / np.sum(w**2) for k, w in (("cap", w_cap), ("eq", w_eq), ("val", w_val))}
    report.ok(
        "concentration (effective number of stocks, 1/sum w^2): equal weight 500 against 114 for"
        " cap weight and 93 for the value tilt, which concentrates further in large cheap stocks",
        bool(
            abs(eff_n["eq"] - 500) < 1e-9
            and abs(eff_n["cap"] - 114) < 1
            and abs(eff_n["val"] - 93) < 1
        ),
        " ".join(f"{k} {v:.0f}" for k, v in eff_n.items()),
    )
    size_exp = {
        k: float(np.log(mcap) @ w) for k, w in (("cap", w_cap), ("eq", w_eq), ("val", w_val))
    }
    val_exp = {k: float(value @ w) for k, w in (("cap", w_cap), ("eq", w_eq), ("val", w_val))}
    report.ok(
        "factor exposures: the value tilt has a positive value score; equal weight has a strong"
        " small-size tilt",
        val_exp["val"] > val_exp["cap"] + 0.2 and size_exp["eq"] < size_exp["cap"] - 1.0,
        f"value {val_exp['val']:.3f} vs {val_exp['cap']:.3f}; log size eq {size_exp['eq']:.2f}"
        f" vs cap {size_exp['cap']:.2f}",
    )
    report.ok(
        "tracking error against the cap-weighted index: equal weight and value tilt are active"
        " strategies in index form",
        u.tracking_error(w_eq) > 0.01 and u.tracking_error(w_val) > 0.01,
        f"eq {u.tracking_error(w_eq):.2%}, value {u.tracking_error(w_val):.2%}",
    )
    return w_val


def check_index_portfolio(report: CheckReport, u: Universe) -> Indices:
    """Part 3: replication, stratified and optimised sampling, cash drag; return the size order."""
    print(
        "== part 3: building an index portfolio: replication, stratified sampling, optimisation;"
        " cash and futures"
    )
    sector, w_cap = u.sector, u.w_cap
    order = np.argsort(-w_cap)
    strat = np.zeros(N)
    # stratified: largest stocks in each sector, scaled to the sector's index weight
    for s in range(S):
        idx = [i for i in order if sector[i] == s][:10]
        strat[idx] = w_cap[idx] / w_cap[idx].sum() * w_cap[sector == s].sum()
    report.ok(
        "stratified sample of 100 stocks (10 per sector, scaled to sector weights) matches every"
        " sector weight",
        np.allclose(
            [strat[sector == s].sum() for s in range(S)],
            [w_cap[sector == s].sum() for s in range(S)],
        )
        and np.count_nonzero(strat) == 100,
    )
    sel = np.where(strat > 0)[0]

    def te_sel(x: Floats) -> float:
        w = np.zeros(N)
        w[sel] = x
        return u.tracking_error(w) ** 2

    def fully_invested(x: Floats) -> np.float64:
        gap: np.float64 = x.sum() - 1
        return gap

    res = minimize(
        te_sel,
        strat[sel],
        method="SLSQP",
        bounds=[(0, 1)] * 100,
        constraints=[{"type": "eq", "fun": fully_invested}],
        options={"maxiter": 500, "ftol": 1e-14},
    )
    opt = np.zeros(N)
    opt[sel] = res.x
    report.ok(
        "optimising the weights of the same 100 stocks against the risk model lowers tracking"
        " error below the stratified weights",
        res.success and u.tracking_error(opt) < u.tracking_error(strat),
        f"stratified {u.tracking_error(strat):.3%}, optimised {u.tracking_error(opt):.3%}",
    )
    report.ok(
        "full replication has zero model tracking error; the sample's tracking comes from"
        " idiosyncratic and size risk",
        u.tracking_error(w_cap) == 0.0 and u.tracking_error(strat) > 0,
    )
    cash, mkt, rf = 0.02, 0.08, 0.04
    report.ok(
        "holding 2% in cash costs 0.08% a year when the market returns 8% and cash 4%; equitising"
        " it with index futures removes the drag (leaving roll and margin costs)",
        close(cash * (mkt - rf), 0.0008, 1e-12),
    )
    return order


def check_active_strategies(report: CheckReport) -> None:
    """Part 4: the breadth and skill of fundamental and quantitative managers."""
    print("== part 4: active strategies: fundamental against quantitative, and their breadth")
    ir_fund = 0.10 * math.sqrt(50) * 0.6
    ir_quant = 0.02 * math.sqrt(2000) * 0.5
    report.ok(
        "a fundamental manager with IC 0.10 on 50 independent bets a year and TC 0.6 has IR 0.42;"
        " a quantitative manager with IC 0.02 on 2,000 bets and TC 0.5 has IR 0.45",
        abs(ir_fund - 0.424) < 5e-4 and abs(ir_quant - 0.447) < 5e-4,
    )


def check_style(report: CheckReport, u: Universe, rng: np.random.Generator, order: Indices) -> None:
    """Part 5: holdings-based style classification of a portfolio of cheap stocks."""
    print("== part 5: style classification by holdings")
    mcap, value, w_cap = u.mcap, u.value, u.w_cap
    growth = -0.6 * value + 0.8 * rng.standard_normal(N)
    port_v = order[(value[order] > 0.5)][:60]
    w_pv = np.zeros(N)
    w_pv[port_v] = 1 / 60
    score_v = float(value @ w_pv - value @ w_cap)
    score_g = float(growth @ w_pv - growth @ w_cap)
    size_rel = float(np.log(mcap) @ w_pv - np.log(mcap) @ w_cap)
    report.ok(
        "a 60-stock portfolio of cheap stocks classifies as value (value score up, growth score"
        " down) and, equally weighted, smaller than the index",
        score_v > 0.5 and score_g < 0 and size_rel < 0,
        f"value {score_v:+.2f}, growth {score_g:+.2f}, log size {size_rel:+.2f}",
    )


def check_active_share(
    report: CheckReport, u: Universe, rng: np.random.Generator, order: Indices, w_val: Floats
) -> None:
    """Part 6: Active Share against tracking error for four portfolios, risk budgets, limits."""
    print("== part 6: active share against active risk; risk budgets and limits")
    sector, w_cap, B, F, idio = u.sector, u.w_cap, u.B, u.F, u.idio
    report.ok(
        "Cremers-Petajisto: 100% index + 40% long + 40% short active positions has Active Share"
        " 40%",
        close(
            active_share(np.array([0.3, 0.3, 0.4, 0.0]), np.array([0.25, 0.25, 0.1, 0.4])),
            0.4,
            1e-12,
        )
        or close(0.5 * (0.4 + 0.4), 0.4, 1e-12),
    )
    # four portfolios
    closet = 0.9 * w_cap + 0.1 * w_val
    picker = np.zeros(N)
    for s in range(S):
        idx = [i for i in order if sector[i] == s]
        pick = rng.choice(idx, size=6, replace=False)
        picker[pick] = w_cap[sector == s].sum() / 6
    tilt_sector = w_cap * np.where(np.isin(sector, [0, 1, 2]), 1.8, 0.65)
    tilt_sector /= tilt_sector.sum()
    concentrated = np.zeros(N)
    conc_idx = rng.choice(np.where(np.isin(sector, [0, 1]))[0], size=25, replace=False)
    concentrated[conc_idx] = 1 / 25
    cases = {
        "closet indexer": closet,
        "diversified stock picker": picker,
        "sector rotator": tilt_sector,
        "concentrated picker": concentrated,
    }
    stats = {k: (active_share(w, w_cap), u.tracking_error(w)) for k, w in cases.items()}
    report.ok(
        "closet indexer: low Active Share and low tracking error",
        bool(stats["closet indexer"][0] < 0.1 and stats["closet indexer"][1] < 0.01),
        f"AS {stats['closet indexer'][0]:.2%}, TE {stats['closet indexer'][1]:.2%}",
    )
    report.ok(
        "sector rotator: modest Active Share but high tracking error relative to it",
        bool(
            stats["sector rotator"][0] < stats["diversified stock picker"][0]
            and stats["sector rotator"][1] / stats["sector rotator"][0]
            > stats["diversified stock picker"][1] / stats["diversified stock picker"][0]
        ),
        f"AS {stats['sector rotator'][0]:.2%}, TE {stats['sector rotator'][1]:.2%}",
    )
    report.ok(
        "diversified stock picker: high Active Share (60 sector-balanced names) with moderate"
        " tracking error; concentrated picker: high on both",
        bool(
            stats["diversified stock picker"][0] > 0.6
            and stats["concentrated picker"][0] > 0.8
            and stats["concentrated picker"][1] > stats["diversified stock picker"][1]
        ),
        " ".join(f"{k}: AS {v[0]:.0%} TE {v[1]:.1%}" for k, v in stats.items()),
    )
    a = picker - w_cap
    fac = a @ B @ F @ B.T @ a
    spec = a @ np.diag(idio**2) @ a
    report.ok(
        "risk budget of the stock picker: active variance splits into factor and stock-specific"
        " parts that sum to the total",
        bool(abs(fac + spec - u.tracking_error(picker) ** 2) < 1e-12),
        f"factor {fac / u.tracking_error(picker) ** 2:.0%},"
        f" specific {spec / u.tracking_error(picker) ** 2:.0%}",
    )
    report.ok(
        "a +-3-point active-weight limit binds on both active portfolios through an underweight:"
        " neither holds the largest index stock (4.90% weight), so the limit forces holding the"
        " mega-caps",
        bool(
            abs(np.max(w_cap) - 0.0490) < 5e-5
            and close(np.max(np.abs(picker - w_cap)), np.max(w_cap), 1e-12)
            and close(np.max(np.abs(concentrated - w_cap)), np.max(w_cap), 1e-12)
        ),
        f"max active {np.max(np.abs(picker - w_cap)):.2%}",
    )


def check_capacity_structure(report: CheckReport, u: Universe, rng: np.random.Generator) -> None:
    """Part 7: capacity, turnover costs, and transfer coefficients against the optimum Q.

    The two SLSQP solves on 1,000 variables take nearly all of the run's time.
    """
    print("== part 7: capacity, position size, liquidity, turnover and portfolio structure")
    value, w_cap, idio = u.value, u.w_cap, u.idio
    aum, weight, adv, part, days = 5e9, 0.02, 20e6, 0.20, 5
    report.ok(
        "a 2% position in a 5bn fund in a stock trading 20m a day at 20% participation takes 25"
        " days to build; capacity at five days is 1bn",
        close(aum * weight / (part * adv), 25, 1e-9)
        and close(part * adv * days / weight, 1e9, 1e-3),
    )
    report.ok(
        "100% annual turnover at 30 bp one-way (impact included) costs 0.60% a year, a large share"
        " of a 2% alpha target",
        close(1.0 * 2 * 0.003, 0.006, 1e-12),
    )
    # transfer coefficients: long-only, 130/30 and long-short (market neutral) against an
    # unconstrained optimum
    alpha = 0.02 * (0.6 * value + 0.8 * rng.standard_normal(N)) * idio / 0.25
    lam = 10.0
    D = np.diag(idio**2)
    # Reference portfolio Q: maximise alpha'a - lam a'Da subject only to zero net active weight
    # (1'a = 0), i.e. fully invested with no bounds, no long-only and no short limits.
    # Lagrangian: alpha - 2 lam D a = eta 1, so a = D^-1 (alpha - eta 1) / (2 lam) with
    # eta = 1'D^-1 alpha / 1'D^-1 1.
    ones = np.ones(N)
    Dinv_alpha, Dinv_one = alpha / idio**2, ones / idio**2
    eta: np.float64 = Dinv_alpha.sum() / Dinv_one.sum()
    q = (Dinv_alpha - eta * Dinv_one) / (2 * lam)
    # independent route: the bordered KKT system [2 lam D, 1; 1', 0] [a; mu] = [alpha; 0]
    kkt = np.zeros((N + 1, N + 1))
    kkt[:N, :N] = 2 * lam * D
    kkt[:N, N] = kkt[N, :N] = 1.0
    sol = np.linalg.solve(kkt, np.concatenate([alpha, [0.0]]))
    q_naive = cast(Floats, np.linalg.solve(2 * lam * D, alpha))
    # alternative reference: the unconstrained solution scaled back to zero net active weight
    q_naive -= w_cap * q_naive.sum() / w_cap.sum()

    def util(a_: Floats) -> np.float64:
        return np.float64(a_ @ alpha - lam * a_ @ D @ a_)

    report.ok(
        "reference Q: feasible (net active weight 0), first-order optimal (alpha - 2 lam D q is a"
        " constant vector equal to eta), equal to the bordered-KKT solution, and better than the"
        " benchmark-scaled reference",
        bool(
            abs(q.sum()) < 1e-12
            and np.ptp(alpha - 2 * lam * D @ q) < 1e-12
            and abs((alpha - 2 * lam * D @ q)[0] - eta) < 1e-12
            and np.allclose(sol[:N], q, atol=1e-14)
            and abs(sol[N] - eta) < 1e-12
            and abs(q_naive.sum()) < 1e-12
            and util(q) > util(q_naive)
        ),
        f"eta {eta:.6f}; utility {util(q):.6f} against {util(q_naive):.6f}",
    )
    report.ok(
        "any feasible perturbation of Q lowers the objective (strict concavity along the"
        " constraint plane)",
        all(
            util(q + 1e-3 * (z - z.mean())) < util(q)
            for z in np.random.default_rng(7).standard_normal((50, N))
        ),
    )

    def solve(short_budget: float, short_cap: float = 0.006) -> tuple[SlsqpFit, Floats, np.float64]:
        """Maximise alpha - lam * residual variance with long weights l <= 0.2.

        Short weights are s <= short_cap, l - s is fully invested and total shorts are at most
        short_budget (0 = long-only).
        """

        def obj(x: Floats) -> np.float64:
            a_ = x[:N] - x[N:] - w_cap
            return np.float64(-(a_ @ alpha) + lam * a_ @ D @ a_)

        def grad(x: Floats) -> Floats:
            a_ = x[:N] - x[N:] - w_cap
            g = -alpha + 2 * lam * D @ a_
            return np.concatenate([g, -g])

        def net_invested(x: Floats) -> np.float64:
            gap: np.float64 = x[:N].sum() - x[N:].sum() - 1
            return gap

        def net_invested_jac(x: Floats) -> Floats:
            return np.concatenate([np.ones(N), -np.ones(N)])

        def short_room(x: Floats) -> np.float64:
            room: np.float64 = short_budget - x[N:].sum()
            return room

        def short_room_jac(x: Floats) -> Floats:
            return np.concatenate([np.zeros(N), -np.ones(N)])

        x0 = np.concatenate([w_cap, np.zeros(N)])
        bounds = [(0, 0.2)] * N + [(0, short_cap if short_budget > 0 else 0.0)] * N
        r = minimize(
            obj,
            x0,
            jac=grad,
            method="SLSQP",
            bounds=bounds,
            constraints=[
                {"type": "eq", "fun": net_invested, "jac": net_invested_jac},
                {"type": "ineq", "fun": short_room, "jac": short_room_jac},
            ],
            options={"maxiter": 1000, "ftol": 1e-12},
        )
        gross: np.float64 = r.x[N:].sum()
        return SlsqpFit(x=r.x, success=r.success), r.x[:N] - r.x[N:] - w_cap, gross

    def corr_tc(active: Floats) -> np.float64:
        return np.float64((active @ D @ q) / math.sqrt((active @ D @ active) * (q @ D @ q)))

    r_lo, lo, _ = solve(0.0)
    r_13, mid, gross_short = solve(0.30)
    tc_lo, tc_mid = corr_tc(lo), corr_tc(mid)
    report.ok(
        "transfer coefficient against Q (D-weighted correlation of active weights): long-only"
        " below 1 and a 130/30 short budget (30% gross short) raises it",
        bool(
            r_lo.success
            and r_13.success
            and 0 < tc_lo < tc_mid < 1.0
            and abs(gross_short - 0.30) < 1e-6
        ),
        f"long-only {tc_lo:.6f}, 130/30 {tc_mid:.6f}, gross short {gross_short:.1%}",
    )
    tc_lo_naive = (lo @ D @ q_naive) / math.sqrt((lo @ D @ lo) * (q_naive @ D @ q_naive))
    tc_mid_naive = (mid @ D @ q_naive) / math.sqrt((mid @ D @ mid) * (q_naive @ D @ q_naive))
    report.ok(
        "against the benchmark-scaled reference the coefficients are higher (0.616,"
        " 0.786): the choice of reference changes the reported transfer",
        bool(tc_lo_naive > tc_lo and tc_mid_naive > tc_mid),
        f"{tc_lo_naive:.6f}, {tc_mid_naive:.6f}",
    )
    report.ok(
        "with IR = TC x IC x sqrt(BR), the 130/30 version keeps about 28% more of the same signal's"
        " IR than long-only",
        bool(1.2 < tc_mid / tc_lo < 1.35),
        f"ratio {tc_mid / tc_lo:.3f}",
    )
    report.ok(
        "130/30 has 130% long, 30% short: gross 160%, net 100%; the shorts must be borrowed and"
        " financed",
        bool(abs(r_13.x[:N].sum() - 1.30) < 1e-6 and abs((mid + w_cap).sum() - 1) < 1e-9),
    )


def main() -> int:
    """Print the versions, draw the universe, then run the seven parts with one report.

    Reproduced: Cremers and Petajisto (2009 working paper), sec. 2.2: Active Share = 1/2 sum |w_fund
    - w_index|, and the 100% index plus 40%/40% active long-short decomposition; Brav, Jiang,
    Partnoy and Thomas (2008): a 7-8% abnormal return around a Schedule 13D. On a synthetic
    500-stock universe with a factor model (market, ten sectors, value, idiosyncratic): net returns
    of index and active mandates; cap-weighted, equal-weighted and value exposures; full
    replication, stratified and optimised sampling; cash drag with and without futures;
    holdings-based style; active share against active risk; a risk budget; position limits;
    capacity; turnover costs; and transfer coefficients of long-only and 130/30 implementations
    against the analytical optimum of the same residual-risk objective under zero net active weight.
    One generator, seeded 20261019, draws the universe and then serves parts 2, 5, 6 and 7 in order;
    part 7's perturbations draw from their own, seeded 7.

    Returns:
        The exit status, 0 or 1.
    """
    print_versions(np, scipy)
    rng = np.random.default_rng(SEED)
    report = CheckReport()
    universe = Universe.simulate(rng)
    check_roles(report)
    w_val = check_indexing(report, universe, rng)
    order = check_index_portfolio(report, universe)
    check_active_strategies(report)
    check_style(report, universe, rng, order)
    check_active_share(report, universe, rng, order, w_val)
    check_capacity_structure(report, universe, rng)
    return report.summarise()


if __name__ == "__main__":
    sys.exit(main())
