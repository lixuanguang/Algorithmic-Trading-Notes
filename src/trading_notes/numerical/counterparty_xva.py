"""Counterparty credit risk: exposures, CVA, wrong-way risk, collateral and rate-tree CVA.

Library gap-filling Batch L2, package P7 (2026-10-21): the worked examples of
def:counterparty-exposure-measures, meth:credit-valuation-adjustment, def:wrong-way-risk and the
rate-tree extension of meth:risky-bond-cva.

Part 1 reproduces published examples: Gregory's normal-distribution EE and PFE (The xVA Challenge,
3rd ed., sec. 7.2.4, p. 116), his CVA of a square-root exposure (sec. 14.2.4, p. 312), and the gold
forward of Hull (Options, Futures, and Other Derivatives, 11th Global ed., Example 24.6) and Hull
(Risk Management and Financial Institutions, 6th ed., Example 18.3). Part 2 is the one-date
wrong-way-risk example: V ~ N(0, 1), default when a latent normal Y with Corr(V, Y) = rho falls
below Phi^-1(PD) (lower-tail default), PD = 5 percent, R = 40 percent, unit discounting. Part 3
simulates swap exposures under one-factor Hull-White on the GSW curve of 30 September 2026, the
model and curve of short-rate-model-checks.py (a = 0.1, sigma = 1 percent; illustrative). The swaps
are single-curve and synthetic. Part 4 is the rate-tree CVA and risky floater: an original
derivation on the Handbook's calibrated tree (Fabozzi, Handbook of Fixed Income Securities, 9th ed.,
chap. 36), with original credit inputs.

Conventions fixed before the first run: unilateral CVA from the bank's side; exposure max(V, 0) of
the netting set's ex-coupon mark-to-market; risk-neutral measure with the bank-account numeraire.
Two-way CSA in cash, daily variation margin, zero threshold and minimum transfer amount, no initial
margin; collateral C(t) = V(t - delta) for t >= delta and 0 before, held by the bank when positive;
no margin moves in the margin period of risk; posted collateral not segregated; collateral earns the
discount rate and accrual during the MPR is ignored. delta = 10 business days (10/252 years).
Exposure dates are mid-months (plus nine daily dates before delta), so no swap payment falls in any
window (t - delta, t]; the script asserts this for every lag it uses. Default is independent of
rates, with a deterministic hazard. Seeds: 20261071 wrong-way Monte Carlo, 20261072 swap paths,
20261073 PFE bootstrap.

L2 correction pass (2026-10-21): the Hull-White discount factor's sign was corrected (see disc),
with deterministic checks that reject the previous sign; Part 1 adds the units of Gregory's EPE x
spread approximation and a non-unit discount example. Seeds, inputs and tolerances of the original
checks are unchanged. Each generator is made in the part that draws from it, from its own seed; part
3 draws the swap paths and then the PFE bootstrap from its own generator, and part 3b reads the
exposures that part 3 returns.

Run: uv run --frozen --no-editable python -m trading_notes.numerical.counterparty_xva
(numpy, scipy). Exits 1 on failure.
"""

# standard library imports
import itertools
import math
import sys
from typing import Final

# third party library imports
import numpy as np
import scipy
from numpy.typing import NDArray
from scipy import integrate, optimize, stats

# project library imports
from trading_notes.numerical.report import CheckReport

type Floats = NDArray[np.float64]

N: Final = stats.norm.cdf
N_PDF: Final = stats.norm.pdf
GSW: Final = (
    2.220637762132e-14,
    3.9277698129101,
    5.27031980138786,
    17.0928160768659,
    1.86454967884118,
    15.7025187144884,
)
B0: Final = GSW[0] / 100
B1: Final = GSW[1] / 100
B2: Final = GSW[2] / 100
B3: Final = GSW[3] / 100
T1: Final = GSW[4]
T2: Final = GSW[5]
HW_A: Final = 0.1  # Hull-White mean reversion
HW_SG: Final = 0.01  # Hull-White volatility
NOTIONAL: Final = 100.0
DELTA: Final = 10 / 252  # the margin period of risk, in years
PAY_DATES: Final = (1.0, 2.0, 3.0, 4.0, 5.0)
N_PATHS: Final = 40_000
PAR: Final = (0.035, 0.042, 0.047, 0.052)


def lag_windows() -> dict[int, float]:
    """The margin periods of the lag diagnostic, in years, keyed by days."""
    return {5: 5 / 252, 10: 10 / 252, 20: 20 / 252}


def expo_dates() -> list[float]:
    """The exposure dates: nine daily dates, then mid-months for five years."""
    return [k / 252 for k in range(1, 10)] + [(m + 0.5) / 12 for m in range(60)]


def crossing_dates(lag: float, dates: list[float]) -> list[float]:
    """The exposure dates whose window (t - lag, t] contains a payment date."""
    return [t for t in dates if any(t - lag < p <= t for p in PAY_DATES) and t >= lag]


def diagnostic_dates() -> list[float]:
    """The exposure dates whose windows, for every lag, contain no payment date."""
    dates = expo_dates()
    lags = lag_windows()
    crossing = {lag: crossing_dates(d, dates) for lag, d in lags.items()}
    return [t for t in dates if t >= lags[20] and not any(t in crossing[g] for g in lags)]


def fwd(t: float) -> float:
    """Instantaneous forward rate of the GSW curve at t."""
    e1, e2 = math.exp(-t / T1), math.exp(-t / T2)
    return B0 + B1 * e1 + B2 * (t / T1) * e1 + B3 * (t / T2) * e2


def zero_yield(t: float) -> float:
    """Zero-coupon yield of the GSW curve at t."""
    if t == 0:
        return fwd(0.0)
    x1, x2 = t / T1, t / T2
    g1, g2 = (1 - math.exp(-x1)) / x1, (1 - math.exp(-x2)) / x2
    return B0 + B1 * g1 + B2 * (g1 - math.exp(-x1)) + B3 * (g2 - math.exp(-x2))


def P0(t: float) -> float:
    """Discount factor P(0, t) of the GSW curve."""
    return math.exp(-zero_yield(t) * t)


def bfun(tau: float) -> float:
    """The Hull-White B function (1 - e^{-a tau}) / a."""
    return (1 - math.exp(-HW_A * tau)) / HW_A


def alpha(t: float) -> float:
    """Return the Hull-White drift that fits the initial curve at time t."""
    return fwd(t) + HW_SG**2 / (2 * HW_A**2) * (1 - math.exp(-HW_A * t)) ** 2


def bond(t: float, T: float, x: Floats) -> Floats:
    """Hull eqs. (32.6)-(32.8): P(t, T) given the short rate r = x + alpha(t) on each path."""
    if T <= t:
        return np.ones_like(x)
    B = bfun(T - t)
    lnA = (
        math.log(P0(T) / P0(t))
        + B * fwd(t)
        - HW_SG**2
        / (4 * HW_A**3)
        * (math.exp(-HW_A * T) - math.exp(-HW_A * t)) ** 2
        * (math.exp(2 * HW_A * t) - 1)
    )
    return np.exp(lnA - B * (x + alpha(t)))


def var_int(t: float) -> float:
    """Var(int_0^t x du) for the Ornstein-Uhlenbeck factor x with x(0) = 0."""
    return HW_SG**2 / HW_A**2 * (t - 2 * bfun(t) + (1 - math.exp(-2 * HW_A * t)) / (2 * HW_A))


def disc(t: float, integ: float | Floats) -> Floats:
    """D(0, t) = exp(-int_0^t r du) with r = x + alpha and I = int_0^t x du.

    E[x] = 0, so the mean short-rate integral is int_0^t alpha du = -ln P0(t) + var_int(t) / 2, and
    D(0, t) = P0(t) exp(-var_int(t) / 2 - I). Since I ~ N(0, var_int(t)), E[D(0, t)] = P0(t).
    """
    return P0(t) * np.exp(-0.5 * var_int(t) - integ)


def par_rate(n: int) -> float:
    """The par swap rate of an annual n-year swap on the GSW curve."""
    return (1 - P0(n)) / sum(P0(j) for j in range(1, n + 1))


def swap_value(
    t: float, x: Floats, last_reset_bond: Floats, K: float, n: int, payer: bool = True
) -> Floats:
    """Return the ex-coupon value at t of an annual swap, fixed K and floating set in advance."""
    if t >= n:
        return np.zeros_like(x)
    k = math.floor(t)  # last reset at k (k = 0 uses today's curve)
    nxt = bond(t, k + 1, x)
    floating = nxt / last_reset_bond - bond(t, n, x)
    fixed = K * sum(bond(t, j, x) for j in range(k + 1, n + 1))
    return NOTIONAL * (floating - fixed) * (1 if payer else -1)


def calibrate(par: tuple[float, ...] | list[float], sigma: float) -> list[Floats]:
    """Return the lowest one-year rate at each date so each par bond prices at 100 (chap. 36)."""
    rates: list[Floats] = [np.array([par[0]])]
    for n in range(2, len(par) + 1):
        cpn = 100 * par[n - 1]

        def price(r_low: float) -> float:
            tree = [*rates, r_low * np.exp(2 * sigma * np.arange(n))]
            val = np.full(n + 1, 100 + cpn)
            for t in range(n - 1, -1, -1):
                val = 0.5 * (val[:-1] + val[1:]) / (1 + tree[t]) + (cpn if t > 0 else 0)
            return float(val[0]) - 100

        rates.append(
            optimize.brentq(price, 1e-6, 0.5, xtol=1e-15, rtol=1e-15)
            * np.exp(2 * sigma * np.arange(n))
        )
    return rates


def state_prices(tree: list[Floats]) -> list[Floats]:
    """Return Arrow-Debreu prices AD[t][j] of a unit paid at node (t, j), one-half per branch."""
    ad: list[Floats] = [np.array([1.0])]
    for t in range(len(tree)):
        nxt = np.zeros(t + 2)
        nxt[:-1] += 0.5 * ad[t] / (1 + tree[t])
        nxt[1:] += 0.5 * ad[t] / (1 + tree[t])
        ad.append(nxt)
    return ad


def bond_values(tree: list[Floats], cpn: float, n: int) -> list[Floats]:
    """Return the ex-coupon value of an n-year bond at each node of dates 0..n."""
    vals: list[Floats] = [np.zeros(0)] * (n + 1)
    vals[n] = np.zeros(n + 1)
    nxt = np.full(n + 1, 100 + cpn)
    for t in range(n - 1, -1, -1):
        vals[t] = 0.5 * (nxt[:-1] + nxt[1:]) / (1 + tree[t])
        nxt = vals[t] + cpn
    return vals


def tree_cva(tree: list[Floats], cpn: float, hazard: list[float], R: float) -> float:
    """Return the tree CVA, with default just before each date-t payment."""
    n = len(tree)
    vals, ad = bond_values(tree, cpn, n), state_prices(tree)
    surv = [math.exp(-sum(hazard[:t])) for t in range(n + 1)]
    return sum(
        (surv[t - 1] - surv[t]) * float(ad[t] @ (vals[t] + cpn + (100 if t == n else 0) - R * 100))
        for t in range(1, n + 1)
    )


def path_cva(tree: list[Floats], cpn: float, hazard: list[float], R: float) -> float:
    """The same CVA by listing all 2^n paths and discounting the expected loss along each."""
    n = len(tree)
    vals = bond_values(tree, cpn, n)
    surv = [math.exp(-sum(hazard[:t])) for t in range(n + 1)]
    total = 0.0
    for path in itertools.product((0, 1), repeat=n):
        j, disc_f, pv = 0, 1.0, 0.0
        for t in range(1, n + 1):
            disc_f /= 1 + tree[t - 1][j]
            j += path[t - 1]
            expo = vals[t][j] + cpn + (100 if t == n else 0)
            pv += (surv[t - 1] - surv[t]) * disc_f * (expo - R * 100)
        total += pv / 2**n
    return total


def swap_tree_cva(tree: list[Floats], K: float, hazard: list[float], R: float) -> float:
    """Return the unilateral CVA of a payer swap on the tree, with loss (1 - R) max(V, 0)."""
    n = len(tree)
    fixed, ad = bond_values(tree, 100 * K, n), state_prices(tree)
    surv = [math.exp(-sum(hazard[:t])) for t in range(n + 1)]
    out = 0.0
    for t in range(1, n + 1):
        v_ex = 100 - fixed[t] if t < n else np.zeros(n + 1)  # floating leg ex-coupon is par
        pv = 0.0
        for p_node in range(t):
            w = ad[t - 1][p_node] * 0.5 / (1 + tree[t - 1][p_node])
            net = 100 * (tree[t - 1][p_node] - K)  # the net payment due at t, set at the parent
            pv += w * (max(v_ex[p_node] + net, 0) + max(v_ex[p_node + 1] + net, 0))
        out += (surv[t - 1] - surv[t]) * (1 - R) * pv
    return out


def floater_values(tree: list[Floats], margin: float, dm: float = 0.0) -> list[Floats]:
    """Return the ex-coupon floater values: coupon (r_t + margin) x 100, paid one period later."""
    n = len(tree)
    vals: list[Floats] = [np.zeros(0)] * (n + 1)
    vals[n] = np.zeros(n + 1)
    nxt = np.full(n + 1, 100.0)
    for t in range(n - 1, -1, -1):
        up = nxt[1:] + 100 * (tree[t] + margin)
        dn = nxt[:-1] + 100 * (tree[t] + margin)
        vals[t] = 0.5 * (up + dn) / (1 + tree[t] + dm)
        nxt = vals[t]
    return vals


def floater_cva(tree: list[Floats], margin: float, hazard: list[float], R: float) -> float:
    """Return the CVA of a floater, weighting its coupons and value by state prices and survival."""
    n = len(tree)
    vals, ad = floater_values(tree, margin), state_prices(tree)
    surv = [math.exp(-sum(hazard[:t])) for t in range(n + 1)]
    out = 0.0
    for t in range(1, n + 1):
        coupon = 100 * (tree[t - 1] + margin)  # set at the parent node at t - 1, paid at t
        # exposure at child (t, j): its ex-coupon value plus the coupon set at its parent(s),
        # weighted
        cpn_child = np.zeros(t + 1)
        w = np.zeros(t + 1)
        cpn_child[:-1] += ad[t - 1] * 0.5 / (1 + tree[t - 1]) * coupon
        cpn_child[1:] += ad[t - 1] * 0.5 / (1 + tree[t - 1]) * coupon
        w[:-1] += ad[t - 1] * 0.5 / (1 + tree[t - 1])
        w[1:] += ad[t - 1] * 0.5 / (1 + tree[t - 1])
        red = 100 if t == n else 0
        pv_expo = float(cpn_child.sum() + w @ (vals[t] + red))
        out += (surv[t - 1] - surv[t]) * (pv_expo - R * 100 * float(ad[t].sum()))
    return out


# ---------------------------------------------------------------------------------------------
def check_published(report: CheckReport) -> None:
    """Part 1: published examples of the exposure measures, the CVA and the gold forward.

    Args:
        report: The run's report.
    """
    print("== Part 1: published examples")
    for mu, s, ee_p, pfe_p in ((2.0, 2.0, 2.17, 6.65), (2.0, 4.0, 2.79, 11.31)):
        ee = mu * N(mu / s) + s * N_PDF(mu / s)
        pfe = mu + stats.norm.ppf(0.99) * s
        report.ok(
            f"Gregory p. 116: normal future value (mean {mu:g}, s.d. {s:g}) has EE {ee_p} and 99%"
            " PFE"
            f" {pfe_p}",
            abs(ee - ee_p) < 5e-3 and abs(pfe - pfe_p) < 5e-3,
            f"{ee:.4f}, {pfe:.4f}",
        )
    spread, lgd = 0.03, 0.6

    def ee_g(t: float) -> float:
        return 0.01 * math.sqrt(t)

    def surv(t: float) -> float:
        return math.exp(-spread * t / lgd)

    grid = [0.25 * i for i in range(21)]
    cva_end = lgd * sum(ee_g(b) * (surv(a) - surv(b)) for a, b in itertools.pairwise(grid))
    cva_mid = lgd * sum(
        0.5 * (ee_g(a) + ee_g(b)) * (surv(a) - surv(b)) for a, b in itertools.pairwise(grid)
    )
    cva_exact = lgd * integrate.quad(lambda t: ee_g(t) * spread / lgd * surv(t), 0, 5)[0]
    report.ok(
        "Gregory p. 312: CVA of EE = 1% sqrt(t), 300 bp, LGD 60%, 20 quarterly dates: 0.200%, exact"
        " 0.193%, averaged 0.192%",
        abs(100 * cva_end - 0.200) < 5e-4
        and abs(100 * cva_exact - 0.193) < 5e-4
        and abs(100 * cva_mid - 0.192) < 5e-4,
        f"{100 * cva_end:.4f}%, {100 * cva_exact:.4f}%, {100 * cva_mid:.4f}%",
    )
    F0, K, sg_f, r_f, R_f, T_f = 1600.0, 1500.0, 0.2, 0.05, 0.3, 2.0
    q = (0.02, 0.03)
    v = []
    for t in (0.5, 1.5):
        d1 = (math.log(F0 / K) + sg_f**2 * t / 2) / (sg_f * math.sqrt(t))
        v.append(math.exp(-r_f * T_f) * (F0 * N(d1) - K * N(d1 - sg_f * math.sqrt(t))))
    cva_gold = (1 - R_f) * (q[0] * v[0] + q[1] * v[1])
    report.ok(
        "RMFI Example 18.3: v1 = 132.38, v2 = 186.65, CVA = 5.77 and value 84.71",
        abs(v[0] - 132.38) < 5e-3
        and abs(v[1] - 186.65) < 5e-3
        and abs(cva_gold - 5.77) < 5e-3
        and abs(100 * math.exp(-0.1) - cva_gold - 84.71) < 5e-3,
        f"{v[0]:.2f}, {v[1]:.2f}, {cva_gold:.3f}",
    )
    report.ok(
        "OFOD Example 24.6 prints v1 = 92.67 and v2 = 130.65: the same exposures times (1 - R)",
        abs((1 - R_f) * v[0] - 92.67) < 5e-3 and abs((1 - R_f) * v[1] - 130.65) < 5e-3,
        f"{(1 - R_f) * v[0]:.2f}, {(1 - R_f) * v[1]:.2f}",
    )
    # Added in the L2 correction pass: units of Gregory's EPE x spread (sec. 14.2.5, p. 313). Eq.
    # (14.4) gives CVA "in the same units as the credit spread", a per-annum charge with
    # undiscounted EPE; an upfront CVA is that spread times the risky annuity. Gregory's annuity
    # (zero rates, his online Appendix 14B, not read) is reproduced by (1 - e^{-hT}) / h.
    haz_g = spread / lgd
    annuity = (1 - math.exp(-haz_g * 5)) / haz_g
    cva_bp = 1e4 * cva_end / annuity
    epe_q = sum(ee_g(b) for b in grid[1:]) / 20
    epe_exact = integrate.quad(ee_g, 0, 5)[0] / 5
    approx_bp = 1e4 * epe_q * spread
    report.ok(
        "Gregory p. 313: risky annuity 4.42, CVA spread 0.200% / 4.42 = 4.52 bp a year, EPE 1.54%"
        " (1.49% exact), EPE x 300 bp = 4.62 bp a year",
        abs(annuity - 4.42) < 5e-3
        and abs(cva_bp - 4.52) < 5e-3
        and abs(100 * epe_q - 1.54) < 5e-3
        and abs(100 * epe_exact - 1.49) < 5e-3
        and abs(approx_bp - 4.62) < 5e-3,
        f"{annuity:.4f}, {cva_bp:.4f} bp, {100 * epe_q:.4f}%, {100 * epe_exact:.4f}%,"
        f" {approx_bp:.4f} bp",
    )
    upfront_from_approx = approx_bp / 1e4 * annuity
    report.ok(
        "EPE x spread is a running spread: times the annuity it is within 5% of the 0.200% upfront"
        " CVA, while read as upfront it is about a quarter of it",
        abs(upfront_from_approx / cva_end - 1) < 0.05 and epe_q * spread / cva_end < 0.3,
        f"{100 * upfront_from_approx:.4f}% upfront against {100 * cva_end:.4f}%; EPE x spread"
        f" {100 * epe_q * spread:.4f}% of notional a year",
    )
    # Added in the L2 correction pass: E(t) is undiscounted here, so a default-time exposure enters
    # CVA multiplied by D(0, t). One date at 1 year, exposure 100, PD 5%, R = 40%, deterministic
    # continuously compounded rate 5%.
    pv_cva = (1 - 0.40) * 0.05 * 100 * math.exp(-0.05 * 1)
    report.ok(
        "PV CVA of a one-year exposure of 100 (PD 5%, R 40%, rate 5% continuous) is 2.8536882735,"
        " not 3",
        abs(pv_cva - 2.8536882735) < 1e-10 and abs(pv_cva - 3) > 0.1,
        f"{pv_cva:.10f}",
    )


# ---------------------------------------------------------------------------------------------
def check_wrong_way(report: CheckReport) -> None:
    """Part 2: wrong-way risk at one exposure date, by quadrature and by Monte Carlo.

    Args:
        report: The run's report.
    """
    print("== Part 2: wrong-way risk at one exposure date (200,000 draws)")
    PD, R, s_v = 0.05, 0.40, 1.0
    c = stats.norm.ppf(PD)

    def cva_quad(rho: float) -> float:
        """(1 - R) E[max(V, 0) 1{Y < c}] by quadrature over v of v phi(v) P(Y < c | V = v)."""

        def f(x: float) -> float:
            return s_v * x * N_PDF(x) * N((c - rho * x) / math.sqrt(1 - rho**2))

        return (1 - R) * integrate.quad(f, 0, np.inf, epsabs=1e-14, epsrel=1e-12)[0]

    rhos = (-0.5, -0.25, 0.0, 0.25, 0.5)
    quad_vals = [cva_quad(rho) for rho in rhos]
    rng = np.random.default_rng(20261071)
    z = rng.standard_normal((2, 200_000))
    for rho, qv in zip(rhos, quad_vals, strict=True):
        V = s_v * z[0]
        Y = rho * z[0] + math.sqrt(1 - rho**2) * z[1]
        loss = (1 - R) * np.maximum(V, 0) * (Y < c)
        m, se = float(loss.mean()), float(loss.std(ddof=1) / math.sqrt(loss.size))
        report.ok(
            f"rho = {rho:+.2f}: quadrature CVA {qv:.5f} within 3 s.e. of Monte Carlo",
            abs(m - qv) <= 3 * se,
            f"{m:.5f} (s.e. {se:.5f})",
        )
    indep = (1 - R) * PD * s_v / math.sqrt(2 * math.pi)
    report.ok(
        "at rho = 0 the value equals the independent (1 - R) PD s / sqrt(2 pi) to 1e-10",
        abs(quad_vals[2] - indep) < 1e-10,
        f"{indep:.8f}",
    )
    report.ok(
        "CVA is strictly decreasing in rho (rho < 0: default with high V, wrong-way)",
        all(a > b for a, b in itertools.pairwise(quad_vals)),
        ", ".join(f"{x:.5f}" for x in quad_vals),
    )


# ---------------------------------------------------------------------------------------------
def check_swaps(report: CheckReport) -> tuple[dict[float, Floats], dict[float, Floats]]:
    """Part 3: swap exposures under Hull-White on the GSW curve, from 40,000 simulated paths.

    Args:
        report: The run's report.

    Returns:
        The five-year payer exposures' values and the discounted state, by date, for part 3b.
    """
    print("== Part 3: swap exposure under Hull-White on the GSW curve (40,000 paths)")
    a = HW_A
    sg = HW_SG
    K5, K3 = par_rate(5), par_rate(3)
    lags = lag_windows()
    crossing = {lag: crossing_dates(d, expo_dates()) for lag, d in lags.items()}
    report.ok(
        "no payment falls in (t - 10/252, t] for any exposure date (so V(t) and V(t - delta) share"
        " a"
        " reset)",
        not crossing[10] and not crossing[5],
    )
    diag_dates = diagnostic_dates()
    print(
        f"  20-day windows cross a payment at {len(crossing[20])} dates"
        f" ({', '.join(f'{12 * t:.1f}m' for t in crossing[20])}); they are left out of the lag"
        f" diagnostic for every lag ({len(diag_dates)} common dates)"
    )
    times = sorted(
        set(expo_dates())
        | {t - d for t in expo_dates() for d in lags.values() if t - d > 0}
        | set(PAY_DATES[:-1])
    )
    n_p = N_PATHS
    rng = np.random.default_rng(20261072)
    x = np.zeros(n_p)
    integ = np.zeros(n_p)
    reset_bond: dict[int, Floats] = {0: np.full(n_p, P0(1.0))}
    V5: dict[float, Floats] = {}
    V3: dict[float, Floats] = {}
    D: dict[float, Floats] = {}
    t_prev = 0.0
    for t in times:
        dt = t - t_prev
        e1 = math.exp(-a * dt)
        vx = sg**2 * (1 - e1**2) / (2 * a)
        vi = sg**2 / a**2 * (dt - 2 * bfun(dt) + (1 - e1**2) / (2 * a))
        cv = sg**2 / (2 * a**2) * (1 - e1) ** 2
        L = np.linalg.cholesky(np.array([[vx, cv], [cv, vi]]))
        eps = L @ rng.standard_normal((2, n_p))
        integ = integ + x * bfun(dt) + eps[1]
        x = x * e1 + eps[0]
        t_prev = t
        if t in PAY_DATES:
            reset_bond[round(t)] = bond(t, t + 1, x)
            continue
        k = math.floor(t)
        V5[t] = swap_value(t, x, reset_bond[k], K5, 5, payer=True)
        V3[t] = swap_value(t, x, reset_bond[k], K3, 3, payer=False)
        D[t] = disc(t, integ)
    # Added in the L2 correction pass: deterministic checks of the discount factor. The first run
    # used P0(t) exp(+var_int / 2 - I), which overstates every D(0, t) by exp(var_int(t)), at most
    # 0.29 percent here; the Monte Carlo checks below could not detect it.
    chk = (0.5, 1.96, 4.96)
    int_alpha = [integrate.quad(alpha, 0, t, epsabs=1e-14, epsrel=1e-12)[0] for t in chk]
    err_new = max(
        abs(float(disc(t, 0.0)) / math.exp(-ia) - 1) for t, ia in zip(chk, int_alpha, strict=True)
    )
    err_old = min(
        abs(P0(t) * math.exp(0.5 * var_int(t)) / math.exp(-ia) - 1)
        for t, ia in zip(chk, int_alpha, strict=True)
    )
    report.ok(
        "D(0, t) at I = 0 equals exp(-int alpha) with int alpha by quadrature, to 1e-10 relative"
        " (the"
        " +var/2 sign fails at every date, by more than 1e-6)",
        err_new < 1e-10 and err_old > 1e-6,
        f"error {err_new:.1e}; previous sign {err_old:.2e} or more",
    )
    # Exact-sampling covariance of (x, I), propagated through the simulation's own steps without
    # random numbers. The gap is absolute: var_int is about 1e-13 on the first daily dates, where
    # the closed form loses relative precision, and an absolute variance error e moves D(0, t) by e
    # / 2 relative.
    cov = np.zeros((2, 2))
    var_gap = 0.0
    t_prev = 0.0
    for t in times:
        dt = t - t_prev
        e1 = math.exp(-a * dt)
        step = np.array([[e1, 0.0], [bfun(dt), 1.0]])
        vx = sg**2 * (1 - e1**2) / (2 * a)
        vi = sg**2 / a**2 * (dt - 2 * bfun(dt) + (1 - e1**2) / (2 * a))
        cv = sg**2 / (2 * a**2) * (1 - e1) ** 2
        cov = step @ cov @ step.T + np.array([[vx, cv], [cv, vi]])
        var_gap = max(var_gap, abs(cov[1, 1] - var_int(t)))
        t_prev = t
    mean_d = max(abs(float(disc(t, 0.0)) * math.exp(0.5 * var_int(t)) / P0(t) - 1) for t in chk)
    report.ok(
        "the simulated I has variance var_int(t) at every date (to 1e-14 absolute), so E[D(0, t)] ="
        " P0(t) exactly by the normal moment generating function (to 1e-12)",
        var_gap < 1e-14 and mean_d < 1e-12,
        f"{var_gap:.1e}, {mean_d:.1e}",
    )
    v0 = swap_value(0.0, np.zeros(1), np.array([P0(1.0)]), K5, 5)[0]
    report.ok(
        "the at-market five-year payer swap has V(0) = 0, so EE(0) = 0, to 1e-12",
        abs(v0) < 1e-12,
        f"{v0:.1e}",
    )
    zs = []
    for t in (0.5 / 12, 11.5 / 12, 24.5 / 12, 36.5 / 12, 54.5 / 12):
        # payments after t: floating coupon j is worth P0(j - 1) - P0(j) today whether or not it has
        # been set
        target = NOTIONAL * sum((P0(j - 1) - P0(j)) - K5 * P0(j) for j in range(1, 6) if j > t)
        y = D[t] * V5[t]
        zs.append((float(y.mean()) - target) / float(y.std(ddof=1) / math.sqrt(n_p)))
    report.ok(
        "the discounted ex-coupon swap value has the curve's forward value at five dates (within 4"
        " s.e.)",
        max(abs(z) for z in zs) <= 4,
        "z = " + ", ".join(f"{z:+.2f}" for z in zs),
    )
    mid = [t for t in expo_dates() if t > 0.04]
    EE = np.array([float(np.maximum(V5[t], 0).mean()) for t in mid])
    peak = int(EE.argmax())
    report.ok(
        "EE of the payer swap peaks at an interior date",
        0 < peak < len(mid) - 1,
        f"peak {EE[peak]:.3f} at {mid[peak]:.2f} years; EE at {mid[0]:.2f} and {mid[-1]:.2f} years"
        f" {EE[0]:.3f}, {EE[-1]:.3f}",
    )
    net = {t: V5[t] + V3[t] for t in expo_dates()}
    pathwise = all(
        bool(np.all(np.maximum(net[t], 0) <= np.maximum(V5[t], 0) + np.maximum(V3[t], 0) + 1e-12))
        for t in expo_dates()
    )
    report.ok(
        "netted exposure never exceeds the sum of stand-alone exposures on any path or date",
        pathwise,
    )
    EE_net = np.array([float(np.maximum(net[t], 0).mean()) for t in mid])
    EE_sum = np.array(
        [float(np.maximum(V5[t], 0).mean() + np.maximum(V3[t], 0).mean()) for t in mid]
    )
    report.ok(
        "so netted EE is at most the sum of stand-alone EEs at every date",
        bool(np.all(EE_net <= EE_sum + 1e-12)),
    )
    t_pk = mid[peak]
    pfe = float(np.quantile(np.maximum(V5[t_pk], 0), 0.975))
    rng_b = np.random.default_rng(20261073)
    boot = [
        float(np.quantile(np.maximum(V5[t_pk], 0)[rng_b.integers(0, n_p, n_p)], 0.975))
        for _ in range(200)
    ]
    print(
        f"  97.5% PFE at the EE peak: {pfe:.3f} (bootstrap s.e. {np.std(boot, ddof=1):.3f}, 200"
        f" resamples); netting with the three-year receiver lowers EE at {mid[17]:.2f} years from"
        f" {EE_sum[17]:.3f} to {EE_net[17]:.3f}"
    )
    return V5, D


# ---------------------------------------------------------------------------------------------
def check_collateral(report: CheckReport, V5: dict[float, Floats], D: dict[float, Floats]) -> None:
    """Part 3b: collateral with a ten-day margin period of risk, and the CVA with and without it.

    Args:
        report: The run's report.
        V5: The five-year payer exposures by date, from part 3.
        D: The discount factors by date, from part 3.
    """
    print("== Part 3b: collateral with a 10-day margin period of risk")
    n_p = N_PATHS
    lags = lag_windows()
    expo = expo_dates()
    early = [t for t in expo if t < DELTA]

    def lagged(t: float, d: float) -> Floats:
        return V5[t - d] if t - d > 0 else np.zeros(n_p)

    report.ok(
        "E_c(t) = E(t) for t < delta on every path (no call has settled yet)",
        len(early) == 9
        and all(
            bool(np.all(np.maximum(V5[t] - lagged(t, DELTA), 0) == np.maximum(V5[t], 0)))
            for t in early
        ),
    )
    late = [t for t in expo if t >= DELTA]
    one_way = all(
        bool(np.all(np.maximum(V5[t] - np.maximum(lagged(t, DELTA), 0), 0) <= np.maximum(V5[t], 0)))
        for t in late
    )
    report.ok("one-way variant C = max(V(t - delta), 0): E_c <= E on every path", one_way)
    two_way = all(
        bool(
            np.all(
                np.maximum(V5[t] - lagged(t, DELTA), 0) <= np.abs(V5[t] - lagged(t, DELTA)) + 1e-12
            )
        )
        for t in late
    )
    report.ok(
        "two-way: E_c <= |V(t) - V(t - delta)| on every path, and E_c = 0 when delta = 0", two_way
    )
    posted = sum(int(np.sum((lagged(t, DELTA) < 0) & (V5[t] > 0))) for t in late)
    worse = [
        t
        for t in late
        if float(np.maximum(V5[t] - lagged(t, DELTA), 0).mean())
        > float(np.maximum(V5[t], 0).mean())
    ]
    print(
        f"  path-dates where the bank had posted and V turned positive (E_c > E there): {posted};"
        f" dates with EE_c > EE: {len(worse)}"
    )
    print("  diagnostic, EE_c against sigma_dV / sqrt(2 pi) (common dates, mean over dates):")
    diag_dates = diagnostic_dates()
    for lag, d in lags.items():
        ratio = []
        for t in diag_dates:
            dv = V5[t] - V5[t - d]
            ratio.append(
                float(np.maximum(dv, 0).mean()) / (float(dv.std(ddof=1)) / math.sqrt(2 * math.pi))
            )
        ee_c = np.mean([float(np.maximum(V5[t] - V5[t - d], 0).mean()) for t in diag_dates])
        print(
            f"    {lag:2d} days: mean EE_c {ee_c:.4f}; EE_c / approximation {np.mean(ratio):.3f}"
            f" (range {min(ratio):.3f}-{max(ratio):.3f})"
        )
    h, R_s = 0.02, 0.40
    cva_u = cva_c = 0.0
    gap = []
    for m in range(60):
        t = (m + 0.5) / 12
        pd_m = math.exp(-h * m / 12) - math.exp(-h * (m + 1) / 12)
        ee_star = float((D[t] * np.maximum(V5[t], 0)).mean())
        cva_u += (1 - R_s) * ee_star * pd_m
        cva_c += (1 - R_s) * float((D[t] * np.maximum(V5[t] - lagged(t, DELTA), 0)).mean()) * pd_m
        gap.append(ee_star - P0(t) * float(np.maximum(V5[t], 0).mean()))
    print(
        f"  CVA (hazard 2%, R = 40%, monthly intervals, per 100 notional): uncollateralised"
        f" {cva_u:.10f}, collateralised {cva_c:.10f}; largest |E[D E] - P(0,t) E[E]|"
        f" {max(abs(g) for g in gap):.10f}"
    )


# ---------------------------------------------------------------------------------------------
def check_tree(report: CheckReport) -> None:
    """Part 4: CVA on the Handbook's calibrated rate tree, by nodes and by paths.

    Args:
        report: The run's report.
    """
    print("== Part 4: CVA on the Handbook's calibrated rate tree (original derivation)")
    par = list(PAR)
    tree = calibrate(par, 0.10)
    report.ok(
        "calibrated year-1 and year-3 rates match Handbook Exhibits 36-6 to 36-8 (4.4448, 5.4289;"
        " 5.0483, 9.1986 percent)",
        abs(100 * tree[1][0] - 4.4448) < 5e-5
        and abs(100 * tree[1][1] - 5.4289) < 5e-5
        and abs(100 * tree[3][0] - 5.0483) < 5e-5
        and abs(100 * tree[3][3] - 9.1986) < 5e-4,
    )
    cpn, haz, R_b = 5.0, [0.015] * 4, 0.40
    cva_tree, cva_path = tree_cva(tree, cpn, haz, R_b), path_cva(tree, cpn, haz, R_b)
    report.ok(
        "node-weighted expected exposure gives the same CVA as the pathwise average to 1e-10",
        abs(cva_tree - cva_path) < 1e-10,
        f"{cva_tree:.6f}",
    )
    spot: list[float] = []  # discount factors bootstrapped from the par curve
    for k in range(4):
        spot.append((1 - par[k] * sum(spot)) / (1 + par[k]))
    fwd_rates = [1 / spot[0] - 1] + [spot[t - 1] / spot[t] - 1 for t in range(1, 4)]
    flat_tree = [np.full(t + 1, fwd_rates[t]) for t in range(4)]
    cva_fwd = tree_cva(flat_tree, cpn, haz, R_b)
    gaps = {
        sgm: abs(tree_cva(calibrate(par, sgm), cpn, haz, R_b) - cva_fwd)
        for sgm in (0.2, 0.1, 1e-2, 1e-4)
    }
    report.ok(
        "as sigma -> 0 the tree CVA tends to the forward-rate calculation of meth:risky-bond-cva"
        " (gap"
        " < 1e-6 at sigma = 1e-4)",
        gaps[1e-4] < 1e-6,
        f"forward-rate CVA {cva_fwd:.6f}; gaps "
        + ", ".join(f"{s:g}: {g:.2e}" for s, g in gaps.items()),
    )
    for sgm in (0.0001, 0.10, 0.20):
        print(
            f"  sigma = {sgm:g}: CVA of the 5% four-year bond (hazard 1.5%, R = 40%)"
            f" {tree_cva(calibrate(par, sgm), cpn, haz, R_b):.6f}"
        )
    # Added after the first run, which showed the bond's CVA does not depend on sigma: sum_j
    # AD(t, j) [V(t, j) + C] is the curve value of the flows from t on, so a linear exposure has a
    # curve-determined CVA. A swap's exposure max(V, 0) is not linear, so its CVA should rise with
    # sigma.
    swap_cvas = [
        swap_tree_cva(calibrate(par, sgm), par[-1], haz, R_b) for sgm in (0.0001, 0.10, 0.20)
    ]
    report.ok(
        "an at-market four-year payer swap on the same tree has a CVA that rises with sigma (1e-4,"
        " 10%, 20%)",
        swap_cvas[0] < swap_cvas[1] < swap_cvas[2],
        ", ".join(f"{x:.4f}" for x in swap_cvas),
    )
    fl = floater_values(tree, 0.0)
    report.ok(
        "a default-free floater paying the tree rate flat is worth par at every node to 1e-10",
        all(float(np.max(np.abs(fl[t] - 100))) < 1e-10 for t in range(4)),
    )
    qm, haz_f, R_f2 = 0.005, [0.010, 0.015, 0.020, 0.025], 0.40
    nd_value = float(floater_values(tree, qm)[0][0])
    fair = nd_value - floater_cva(tree, qm, haz_f, R_f2)

    def dm_gap(d: float) -> float:
        return float(floater_values(tree, qm, d)[0][0]) - fair

    dm = optimize.brentq(dm_gap, -0.05, 0.2, xtol=1e-15, rtol=1e-15)
    report.ok(
        "the discount margin solved on the tree reprices the risky floater's fair value to 1e-8",
        abs(float(floater_values(tree, qm, dm)[0][0]) - fair) < 1e-8,
        f"no-default value {nd_value:.4f}, CVA {nd_value - fair:.4f}, fair value {fair:.4f}, quoted"
        f" margin 50 bp, discount margin {1e4 * dm:.2f} bp",
    )


def main() -> int:
    """Print the versions, then run the four parts with one report.

    Returns:
        The exit status, 0 or 1.
    """
    print(f"Python {sys.version.split()[0]}, NumPy {np.__version__}, SciPy {scipy.__version__}")
    report = CheckReport()
    check_published(report)
    check_wrong_way(report)
    V5, D = check_swaps(report)
    check_collateral(report, V5, D)
    check_tree(report)
    if report.failures:
        print("FAILED:", ", ".join(report.failures))
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
