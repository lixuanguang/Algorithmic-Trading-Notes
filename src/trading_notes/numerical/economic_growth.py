"""Economic growth: the worked numbers of four growth entries.

Economic growth (2026-10-19): the worked numbers of def:growth-determinants-factors,
meth:potential-gdp-growth-accounting, mod:growth-theories-convergence and
def:growth-policies-technology-trade.

Reproduced from Economics for Investment Decision Makers (CFA Institute Investment Series,
2013), chap. 11: the S&P 500 decomposition 1946-2007 (Exhibit 11-3, p. 633:
10.82% = 3.01 + 3.94 - 0.12 + 0.32 + 3.67, price appreciation 7.15% against nominal GDP growth
6.95%); the 11% appreciation forecast against 7% nominal growth (Example 11-2, pp. 634-635); the
labour-productivity form 1% + 2% = 3% (eq. 11-5, p. 641); steady-state growth
theta/(1 - alpha) + n for China 6.58%, Japan 0.35% and a third economy 1.41% (Example 11-10,
pp. 666-667). From Mankiw, Macroeconomics, 10th ed. (2019), chap. 9: the AK model's growth
sA - delta (sec. 9-4) and convergence at about 2% a year among similar economies (sec. 9-2).
Original: growth accounting with a TFP residual; diminishing returns in Cobb-Douglas; a
potential-GDP forecast with demographics; a Solow simulation in which saving changes the level
but not the long-run growth of output per worker; convergence of two economies and the model's
convergence speed; a natural-resource windfall that is temporary; and a research externality
that justifies support for R&D.

Count convention: one check is one executed ok() call (a call inside a loop counts once per
iteration).

Run: uv run --frozen --no-editable python -m trading_notes.numerical.economic_growth
(numpy, scipy). Exits 1 on failure.
"""

# standard library imports
import math
import sys
from dataclasses import dataclass
from typing import Final

# third party library imports
import numpy as np
import scipy
from numpy.typing import NDArray
from scipy.optimize import brentq, minimize_scalar

# project library imports
from trading_notes.numerical.report import CheckReport

type Floats = NDArray[np.float64]

# Solow parameters: capital share, depreciation, labour growth and TFP growth. The saving rate
# of the simulations, 0.25 unless stated, is written at each use.
A_S: Final = 1 / 3
D_: Final = 0.05
N_: Final = 0.01
TH_: Final = 0.015


def close(a: float, b: float, tol: float = 1e-9) -> bool:
    """Return whether |a - b| <= tol."""
    return abs(a - b) <= tol


@dataclass(frozen=True)
class SolowPath:
    """One annual path of the per-worker Solow model.

    Attributes:
        y: Output per worker.
        k: Capital per worker at the start of each year.
        k_normalized: Capital per effective worker, k / A^(1/(1 - alpha)).
    """

    y: Floats
    k: Floats
    k_normalized: Floats


def solow_path(s: float, k0: float, years: int = 400, theta: float = TH_) -> SolowPath:
    """Annual Solow model in per-worker terms with TFP growing at theta, from capital k0."""
    a, k = 1.0, k0
    ys: list[float] = []
    raw_k: list[float] = []
    normalized_k: list[float] = []
    for _ in range(years):
        y = a * k**A_S
        ys.append(y)
        raw_k.append(k)
        normalized_k.append(k / a ** (1 / (1 - A_S)))
        k = (s * y + (1 - D_) * k) / (1 + N_)
        a *= 1 + theta
    return SolowPath(np.array(ys), np.array(raw_k), np.array(normalized_k))


def check_asset_returns(report: CheckReport) -> None:
    """Part 1: growth and asset returns."""
    print("== part 1: growth and asset returns")
    parts = {
        "real GDP": 3.01,
        "inflation": 3.94,
        "EPS/GDP": -0.12,
        "P/E": 0.32,
        "dividend yield": 3.67,
    }
    report.ok(
        "Exhibit 11-3 (log returns 1946-2007): 3.01 + 3.94 - 0.12 + 0.32 + 3.67 = 10.82; price"
        " appreciation 7.15 is"
        " nominal GDP 6.95 plus 0.20 from the two ratios; the EPS/GDP term must be -0.12 for the"
        " table to add up",
        close(sum(parts.values()), 10.82, 1e-9)
        and close(parts["real GDP"] + parts["inflation"], 6.95, 1e-9)
        and close(parts["EPS/GDP"] + parts["P/E"], 0.20, 1e-9)
        and not close(3.01 + 3.94 + 0.12 + 0.32 + 3.67, 10.82, 1e-6),
    )
    nominal = 3.25 + 3.75
    report.ok(
        "Example 11-2: 11% forecast appreciation against 7% nominal GDP growth needs 4% a year from"
        " profit share and P/E"
        " forever; a sustainable forecast is 7% appreciation, or 9.5% with the 2.5% dividend yield",
        close(11 - nominal, 4.0) and close(nominal + 2.5, 9.5),
    )


def check_growth_accounting(report: CheckReport) -> None:
    """Part 2: production function, growth accounting and potential GDP."""
    print("== part 2: production function, growth accounting and potential GDP")
    alpha = 0.3
    report.ok(
        "Cobb-Douglas with alpha = 0.3: doubling capital per worker raises output per worker by"
        " 23.1%, and the marginal"
        " product of capital falls by 38.4%: diminishing returns",
        abs(2**alpha - 1 - 0.2311) < 1e-4 and abs(2 ** (alpha - 1) - 1 + 0.3844) < 1e-4,
    )
    gy, gk, gl = 0.030, 0.040, 0.010
    tfp = gy - alpha * gk - (1 - alpha) * gl
    report.ok(
        "growth accounting: output 3.0%, capital 4.0%, labour 1.0%, capital share 0.3: TFP residual"
        " 1.1% (capital"
        " contributes 1.2 points, labour 0.7)",
        close(tfp, 0.011, 1e-12),
    )
    report.ok(
        "EIDM eq. (11-5): labour force +1% and labour productivity +2% give potential growth of 3%",
        close(0.01 + 0.02, 0.03),
    )
    pop_wa, particip, hours, prod = -0.005, 0.003, -0.001, 0.015
    labour = (1 + pop_wa) * (1 + particip) * (1 + hours) - 1
    potential = (1 + labour) * (1 + prod) - 1
    report.ok(
        "potential GDP with demographics: working-age population -0.5%, participation +0.3%, hours"
        " -0.1% give labour"
        " input -0.30%; with productivity +1.5% potential growth is 1.19% a year",
        abs(labour + 0.003013) < 1e-6 and abs(potential - 0.011942) < 1e-6,
        f"labour {labour:.4%}, potential {potential:.4%}",
    )


def check_solow(report: CheckReport) -> float:
    """Part 3: steady states, the Solow simulation and convergence; return its speed lambda."""
    a_s, d_, n_, th_ = A_S, D_, N_, TH_
    print("== part 3: neoclassical (Solow) model, steady state and convergence")
    for name, theta, labour_share, n, target in (
        ("China", 0.025, 0.465, 0.012, 0.0658),
        ("Japan", 0.002, 0.573, 0.0, 0.0035),
        ("third", 0.008, 0.567, 0.0, 0.0141),
    ):
        g_ss = theta / labour_share + n
        report.ok(
            f"Example 11-10 {name}: theta/(1 - alpha) + n = {theta:.1%}/{labour_share} + {n:.1%} ="
            f" {g_ss:.2%}",
            abs(g_ss - target) < 5e-5,
        )
    base = solow_path(0.25, 1.0)
    raw_k, norm_k = base.k, base.k_normalized
    eff_g = (1 + th_) ** (1 / (1 - a_s)) - 1
    norm_star = (0.25 / ((1 + n_) * (1 + eff_g) - (1 - d_))) ** (1 / (1 - a_s))
    report.ok(
        "positive technology: normalized capital converges while raw capital per worker grows",
        bool(
            abs(norm_k[-1] - norm_star) < 1e-6
            and abs(raw_k[-1] / raw_k[-2] - 1 - eff_g) < 1e-7
            and raw_k[-1] > 1000 * norm_k[-1]
        ),
    )
    # Aggregate capital accumulation supplies an independent normalization route.
    K, L, A = 1.0, 1.0, 1.0
    for _ in range(399):
        Y = A * K**a_s * L ** (1 - a_s)
        K = (1 - d_) * K + 0.25 * Y
        L *= 1 + n_
        A *= 1 + th_
    report.ok(
        "aggregate production and capital ledger matches per-worker simulation",
        bool(
            abs(K / L / raw_k[-1] - 1) < 1e-10
            and abs(K / (L * A ** (1 / (1 - a_s))) - norm_star) < 1e-6
        ),
    )
    zero = solow_path(0.25, 1.0, theta=0)
    zero_k, zero_norm = zero.k, zero.k_normalized
    report.ok(
        "zero-technology control: raw and normalized capital coincide and converge",
        bool(
            np.allclose(zero_k, zero_norm)
            and abs(zero_k[-1] - (0.25 / (d_ + n_)) ** (1 / (1 - a_s))) < 1e-5
        ),
    )

    y_lo, y_hi = solow_path(0.20, 1.0).y, solow_path(0.30, 1.0).y
    g_lo, g_hi = y_lo[-1] / y_lo[-2] - 1, y_hi[-1] / y_hi[-2] - 1
    g_theory = (1 + th_) ** (1 / (1 - a_s)) - 1
    report.ok(
        "Solow simulation: long-run growth of output per worker is theta/(1 - alpha) (2.26% in"
        " discrete time) whether the"
        " saving rate is 20% or 30%; the higher saver ends with output per worker 22% higher"
        " (level, not growth)",
        bool(
            abs(g_lo - g_theory) < 1e-4
            and abs(g_hi - g_theory) < 1e-4
            and abs(y_hi[-1] / y_lo[-1] - 1.2247) < 0.01
        ),
        f"growth {g_lo:.4%} / {g_hi:.4%}; level ratio {y_hi[-1] / y_lo[-1]:.4f}",
    )
    y_poor, y_rich = solow_path(0.25, 0.5).y, solow_path(0.25, 8.0).y
    gap = np.log(y_rich / y_poor)
    report.ok(
        "convergence: two economies with the same parameters but capital per worker of 0.5 and 8.0"
        " converge, the poorer"
        " one growing faster; from this large initial gap the log gap halves in about 8 years",
        bool(
            y_poor[1] / y_poor[0] > y_rich[1] / y_rich[0]
            and gap[-1] < 0.001
            and 6 <= int(np.argmax(gap < gap[0] / 2)) <= 10
        ),
        f"half-life {int(np.argmax(gap < gap[0] / 2))} years",
    )
    lam = (1 - a_s) * (n_ + th_ / (1 - a_s) + d_)
    report.ok(
        "near the steady state the model converges at (1 - alpha)(n + g + delta) = 5.5% a year"
        " with alpha = 1/3 (3.5% with a"
        " broad capital share of 2/3), faster than the roughly 2% Mankiw reports among similar"
        " economies",
        abs(lam - 0.0550) < 1e-4
        and abs((1 - 2 / 3) * (n_ + th_ / (1 - 2 / 3) + d_) - 0.0350) < 1e-4,
        f"{lam:.4f}",
    )
    return lam


def check_endogenous_growth(report: CheckReport, lam: float) -> None:
    """Part 4: the AK model, a research externality, a windfall, openness and the golden rule."""
    d_, n_ = D_, N_
    print("== part 4: endogenous growth, policy, resources and openness")
    s_ak, a_ak, d_ak = 0.20, 0.25, 0.03
    report.ok(
        "AK model (Mankiw sec. 9-4): growth = sA - delta = 0.20 x 0.25 - 0.03 = 2.0%; raising"
        " saving to 25% raises growth"
        " permanently to 3.25%, unlike the Solow model",
        close(s_ak * a_ak - d_ak, 0.02, 1e-12) and close(0.25 * a_ak - d_ak, 0.0325, 1e-12),
    )
    # perpetual cash flows: to the firm, and spillovers to others
    cost, private_cf, spill_cf = 100.0, 8.0, 12.0
    npv_private = private_cf / 0.10 - cost
    npv_social = (private_cf + spill_cf) / 0.10 - cost
    subsidy = cost - private_cf / 0.10
    report.ok(
        "research externality: a project costing 100 that returns 8 a year to the firm and 12 to"
        " others has a private NPV"
        " of -20 and a social NPV of +100 at 10%; a subsidy of 20 (20% of cost) makes the firm"
        " indifferent, aligning the"
        " private decision with the social one",
        close(npv_private, -20.0, 1e-9)
        and close(npv_social, 100.0, 1e-9)
        and close(private_cf / 0.10 - (cost - subsidy), 0.0, 1e-9),
    )
    years = np.arange(40)
    resource = np.where(years < 15, 0.04, 0.0)  # windfall adds 4% of GDP for 15 years
    manuf_loss = (
        0.01 * np.minimum(years, 15) / 15
    )  # appreciation erodes tradable sectors, persistent
    net = resource - manuf_loss
    report.ok(
        "a resource windfall worth 4% of GDP for 15 years that erodes tradable output by up to 1%"
        " of GDP (Dutch disease)"
        " adds to income while it lasts but leaves output 1% lower afterwards",
        bool(net[:10].min() > 0 and close(net[-1], -0.01, 1e-12)),
    )
    k_ratio = 1.20
    report.ok(
        "openness: removing barriers to capital lets capital per worker rise 20% in a capital-poor"
        " economy, raising output"
        " per worker 6.3% with alpha = 1/3 during the transition; long-run growth still depends on"
        " TFP",
        abs(k_ratio ** (1 / 3) - 1 - 0.0627) < 1e-4,
    )
    kstar = brentq(lambda k: 0.25 * k ** (1 / 3) - (d_ + n_) * k, 1e-6, 1e6)
    report.ok(
        "steady state without technology growth: s k^alpha = (delta + n) k gives k* ="
        " (s/(delta + n))^(3/2) = 8.51",
        abs(kstar - (0.25 / 0.06) ** 1.5) < 1e-6 and abs(kstar - 8.505) < 1e-3,
        f"{kstar:.4f}",
    )
    report.ok(
        "the golden-rule saving rate equals the capital share: maximising steady-state consumption"
        " (1 - s) k*^alpha over s"
        " gives s = 1/3",
        bool(
            abs(
                minimize_scalar(
                    lambda s: -(1 - s) * (s / 0.06) ** (0.5), bounds=(0.01, 0.99), method="bounded"
                ).x
                - 1 / 3
            )
            < 1e-4
        ),
    )
    report.ok(
        "the implied half-life near the steady state is ln 2 / lambda = 12.6 years",
        abs(math.log(2) / lam - 12.60) < 0.05,
    )


def main() -> int:
    """Print the versions, then run the four parts with one report.

    Returns:
        The exit status, 0 or 1.
    """
    print(f"Python {sys.version.split()[0]}, NumPy {np.__version__}, SciPy {scipy.__version__}")
    report = CheckReport()
    check_asset_returns(report)
    check_growth_accounting(report)
    lam = check_solow(report)
    check_endogenous_growth(report, lam)
    print()
    if report.failures:
        print(f"{len(report.failures)} check(s) failed: {report.failures}")
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
