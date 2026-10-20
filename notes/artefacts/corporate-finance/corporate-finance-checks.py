"""Corporate finance (2026-10-20): the worked numbers of the corporate-finance entries.

The corporate-finance section reuses Harbour Tools plc, the hypothetical IFRS reporter built in
../financial-statement-analysis/statement-analysis-checks.py (EUR millions, valuation date 31 December 2025). That
script is executed here with its output suppressed, so balances, forecasts and the 8.49 discounted-cash-flow value
come from one source. Assumptions added in this batch: a share price of EUR 11.00 at 31 December 2025, a risk-free
rate of 3.0%, an equity risk premium of 5.5%, a peer unlevered beta of 0.93 and a pre-tax cost of debt of 5.2%.
Other companies (Kestrel, the platform, the projects, Company R, Ridgeway) are stand-alone hypothetical examples.

Corrections of 2026-10-20 (audit of PR #31): the WACC weights count the 5m vested options (17.94 at the market
price) in equity; cumulative voting uses N, the total shares voting, with an integer floor and a brute-force
minimality check; the 2025 FCFE reconciliation includes the 6 of equity-issue proceeds; Ridgeway's FCFE is split
into free cash flow before borrowing and actual net borrowing, with cash and debt reconciled and a target-policy
alternative; the acquisition's return on price is compared after tax (6.25%) with the after-tax WACC.

Independent routes: NPV against IRR found by root search; profitability-index ranking against brute-force search
of every project combination; equity value from levered cash flows against firm value less debt (Modigliani-Miller);
EPS after a buyback from the income statement against the earnings-yield rule; Lintner dividends from the
recursion against the closed-form weights; the optimal debt ratio from a grid against the first-order condition;
pro forma ratios from combined statements against the Harbour model's part 21 figures.

Count convention: one check is one executed ok() call (a call inside a loop counts once per iteration).

Run: uv run python corporate-finance-checks.py   (numpy, scipy). Exits 1 on failure.
"""

# standard library imports
import contextlib
import io
import itertools
import runpy
import sys
from pathlib import Path

# third party library imports
import numpy as np
import scipy
from scipy.optimize import brentq

print(f"Python {sys.version.split()[0]}, NumPy {np.__version__}, SciPy {scipy.__version__}")
fails = []
n_checks = 0


def ok(name, cond, detail=""):
    global n_checks
    n_checks += 1
    print(f"  {'ok ' if cond else 'BAD'} {name}{': ' + detail if detail else ''}")
    if not cond:
        fails.append(name)


def close(a, b, tol=1e-9):
    return abs(a - b) <= tol


def npv(rate, flows):
    return sum(c / (1 + rate) ** t for t, c in enumerate(flows))


HARBOUR = (
    Path(__file__).resolve().parent.parent
    / "financial-statement-analysis"
    / "statement-analysis-checks.py"
)
with contextlib.redirect_stdout(io.StringIO()):
    H = runpy.run_path(str(HARBOUR))
B25, R25, TAX = H["B"][2025], H["R"][2025], H["TAX"]
PRICE, SHARES = 11.0, 100.75

# ---------------------------------------------------------------------------------------------
print("== part 1: organisational forms - the tax wedge on distributed and retained profit")
pre_tax, t_corp, t_div, t_pers = 100.0, 0.25, 0.30, 0.40
corp_distributed = pre_tax * (1 - t_corp) * (1 - t_div)
pass_through = pre_tax * (1 - t_pers)
ok(
    "corporation paying out: 100 x 0.75 x 0.70 = 52.50 (effective 47.5%); pass-through at 40% leaves 60",
    close(corp_distributed, 52.5) and close(pass_through, 60.0),
    f"retained in the corporation: {pre_tax * (1 - t_corp):.2f} with personal tax deferred",
)

# ---------------------------------------------------------------------------------------------
print("== part 2: lender and shareholder claims - risk shifting under limited liability")
face = 100.0


def claims(outcomes):
    eq = np.mean([max(v - face, 0.0) for v in outcomes])
    debt = np.mean([min(v, face) for v in outcomes])
    return eq, debt


safe, risky, worse = claims([60, 140]), claims([20, 180]), claims([10, 180])
ok(
    "same mean value 100: the risky project raises equity 20 -> 40 and cuts debt 80 -> 60",
    close(safe[0], 20) and close(safe[1], 80) and close(risky[0], 40) and close(risky[1], 60),
)
ok(
    "a risky project worth 95 is still preferred by shareholders (equity 40) although firm value falls 5",
    close(worse[0], 40) and close(worse[1], 55) and close(sum(worse), 95),
)

# ---------------------------------------------------------------------------------------------
print("== part 3: ownership structures - dual class, pyramids and cumulative voting")
founder_b, public_a, votes_b = 15.0, 85.0, 10
vote_share = founder_b * votes_b / (founder_b * votes_b + public_a)
cash_share = founder_b / (founder_b + public_a)
ok(
    "dual class: 15% of the equity with 10 votes a share carries 63.83% of the votes",
    round(vote_share, 4) == 0.6383 and close(cash_share, 0.15),
)
pyramid_cash = 0.51 * 0.51
diverted = 10.0
ok(
    "pyramid: 51% of a holding company owning 51% gives control with 26.01% of the cash flows; "
    "diverting 10 through a related-party sale costs the controller 2.60 and gains it 10",
    close(pyramid_cash, 0.2601) and round(diverted * pyramid_cash, 2) == 2.6,
)
# Cumulative voting (corrected 2026-10-20): N is the total number of shares voting, not the holder's
# shares. A holder of S shares casts S x D votes; spread over k candidates each gets S D / k, and the other
# holders' (N - S) D votes can give at most (N - S) D / (D - k + 1) to each of D - k + 1 rivals. k seats are
# guaranteed (ties lost) iff S / k > (N - S) / (D - k + 1), i.e. S > N k / (D + 1).
shares_voting, seats = 10_000_000, 5


def guarantees(S, k, N=shares_voting, D=seats):
    """Exact integer test: each of k candidates strictly beats the best D - k + 1 rivals can do."""
    return S * D * (D - k + 1) > (N - S) * D * k


def need_shares(k, N=shares_voting, D=seats):
    return N * k // (D + 1) + 1


ok(
    "cumulative voting: floor(N k/(D+1)) + 1 = 1,666,667 of N = 10m shares voting guarantees one of five seats",
    need_shares(1) == 1_666_667,
)
ok(
    "the threshold is minimal for k = 1..5: it guarantees k seats and one share fewer does not",
    all(
        guarantees(need_shares(k), k) and not guarantees(need_shares(k) - 1, k) for k in range(1, 6)
    ),
    ", ".join(f"k={k}: {need_shares(k):,}" for k in range(1, 6)),
)
ok(
    "the superseded display N/(D+1) + 1 = 1,666,667.67 is not an integer share count",
    round(shares_voting / (seats + 1) + 1, 2) == 1_666_667.67,
)

# ---------------------------------------------------------------------------------------------
print(
    "== part 4: ESG exposure - an emissions cost on Harbour, in cash flows rather than the discount rate"
)
scope12_t = 30_000  # tonnes CO2e a year, illustrative
carbon_price = {
    2026: 80.0,
    2030: 130.0,
}  # EUR per tonne passed through by energy suppliers, illustrative
pass_through_to_customers = 0.4
cost_2030 = scope12_t * carbon_price[2030] / 1e6 * (1 - pass_through_to_customers)
ev_effect = cost_2030 * (1 - TAX) / (0.08 - 0.025) / 1.08**4
ok(
    "30,000 t at EUR 130, 40% passed on: 2.34m a year pre-tax from 2030; capitalised at 8% - 2.5% and discounted "
    "four years, about 23.45m or 0.23 a share",
    round(cost_2030, 2) == 2.34
    and round(ev_effect, 2) == 23.45
    and round(ev_effect / SHARES, 2) == 0.23,
    f"value effect {ev_effect:.2f}",
)

# ---------------------------------------------------------------------------------------------
print("== part 5: business models - a platform's take rate")
bookings, take = 1000.0, 0.20
rev_a = bookings * take
rev_b = bookings * 1.2 * 0.15
ok(
    "cutting the take rate 20% -> 15% needs bookings +33.3% to hold revenue; +20% leaves 180",
    close(rev_a, 200) and close(rev_b, 180) and close(rev_a / (bookings * 0.15) - 1, 1 / 3),
)

# ---------------------------------------------------------------------------------------------
print("== part 6: cash conversion cycle and liquidity (Harbour 2025 against a peer)")
ccc = R25["dso"] + R25["doh"] - R25["dpo"]
ok(
    "Harbour 2025: DSO 58.30 + DIO 107.88 - DPO 91.06 = CCC 75.11 days",
    round(R25["dso"], 2) == 58.30
    and round(R25["doh"], 2) == 107.88
    and round(R25["dpo"], 2) == 91.06
    and round(ccc, 2) == 75.11
    and close(ccc, R25["ccc"]),
)
revenue25, cogs25 = 1080.0, 1080.0 * (1 - R25["gross_margin"])
peer = dict(dso=45.0, dio=70.0, dpo=60.0)
peer_ccc = peer["dso"] + peer["dio"] - peer["dpo"]
release_dio = 10 * cogs25 / 365
ok(
    "peer CCC 55 days; ten fewer inventory days on 2025 cost of sales of 697 would release 19.1",
    close(peer_ccc, 55) and round(cogs25, 0) == 697 and round(release_dio, 1) == 19.1,
)
ok(
    "Harbour liquidity: current 1.84, quick 0.93, cash 0.16",
    [round(R25[k], 2) for k in ("current", "quick", "cash_ratio")] == [1.84, 0.93, 0.16],
)

# ---------------------------------------------------------------------------------------------
print("== part 7: working-capital policy - trade credit and financing seasonal needs")
d, disc_days, net_days = 0.02, 10, 30
simple = d / (1 - d) * 365 / (net_days - disc_days)
ear = (1 / (1 - d)) ** (365 / (net_days - disc_days)) - 1
ok(
    "2/10 net 30: forgoing the discount costs 37.24% simple, 44.59% compounded (365-day year)",
    round(simple, 4) == 0.3724 and round(ear, 4) == 0.4459,
)
lt, st, dep = 0.06, 0.045, 0.025
trough, peak = 160.0, 240.0
matching = trough * lt + (peak - trough) * st * 0.5
conservative = peak * lt - (peak - trough) * dep * 0.5
aggressive = 120 * lt + ((trough - 120) * 0.5 + (peak - 120) * 0.5) * st
ok(
    "financing 160 trough / 240 peak: matching 11.40, conservative 13.40, aggressive 10.80 a year",
    [round(x, 2) for x in (matching, conservative, aggressive)] == [11.4, 13.4, 10.8],
)

# ---------------------------------------------------------------------------------------------
print("== part 8: a capital project - incremental after-tax cash flows, NPV, IRR and ROIC")
WACC = 0.08
capex, wc, salvage, life = 100.0, 15.0, 10.0, 5
rev, var, fixed, cannib, rent_forgone = 130.0, 0.60, 12.0, 5.0, 3.0
dep = (capex - salvage) / life
ebit = rev - var * rev - fixed - cannib - rent_forgone - dep
nopat = ebit * (1 - TAX)
ocf = nopat + dep
flows = [-(capex + wc)] + [ocf] * (life - 1) + [ocf + salvage + wc]
p_npv = npv(WACC, flows)
p_irr = brentq(lambda r: npv(r, flows), -0.5, 1.0)
ok(
    "EBIT 14.00, NOPAT 10.50, operating cash flow 28.50; NPV at 8% 15.81; IRR 12.61%",
    close(ebit, 14) and close(ocf, 28.5) and round(p_npv, 2) == 15.81 and round(p_irr, 4) == 0.1261,
)
ok(
    "NPV is zero at the IRR and positive below it",
    close(npv(p_irr, flows), 0, 1e-9) and npv(0.1, flows) > 0,
)
# The same NPV from a revenue-cost table built line by line (an independent route).
line_flows = []
for t in range(life + 1):
    if t == 0:
        line_flows.append(-capex - wc)
        continue
    pre_tax_cash = rev * (1 - var) - fixed - cannib - rent_forgone
    tax = TAX * (pre_tax_cash - dep)
    line_flows.append(pre_tax_cash - tax + (salvage + wc if t == life else 0.0))
ok("line-by-line cash flows reproduce the NPV", close(npv(WACC, line_flows), p_npv, 1e-9))
sunk_rd = 12.0
interest_aftertax = 0.05 * 50 * (1 - TAX)
npv_with_sunk = p_npv - sunk_rd
npv_double_count = p_npv - sum(interest_aftertax / 1.08**t for t in range(1, 6))
ok(
    "errors: charging sunk R&D 12 gives 3.81; deducting after-tax interest on 50 of debt while discounting at "
    "WACC gives 8.32 (financing counted twice)",
    round(npv_with_sunk, 2) == 3.81 and round(npv_double_count, 2) == 8.32,
)
roic, book = [], capex
for t in range(1, life + 1):
    open_ic, close_ic = book + wc, book - dep + wc
    roic.append(nopat / ((open_ic + close_ic) / 2))
    book -= dep
ok(
    "accounting ROIC rises from 9.91% to 30.88% as the asset depreciates, against a 12.61% IRR",
    round(roic[0], 4) == 0.0991 and round(roic[-1], 4) == 0.3088,
    ", ".join(f"{x:.2%}" for x in roic),
)

# Mutually exclusive projects: scale and timing differences.
A = [-40.0, 22.0, 18.0, 12.0]
Bp = [-100.0, 20.0, 35.0, 45.0, 40.0]
irr_a = brentq(lambda r: npv(r, A), -0.5, 1)
irr_b = brentq(lambda r: npv(r, Bp), -0.5, 1)
cross = brentq(lambda r: npv(r, Bp) - npv(r, A), 0.0, 0.5)
ok(
    "mutually exclusive: A has the higher IRR, B the higher NPV at 8%; NPV profiles cross at 12.39%",
    irr_a > irr_b and npv(WACC, Bp) > npv(WACC, A) and round(cross, 4) == 0.1239,
    f"A NPV {npv(WACC, A):.2f} IRR {irr_a:.2%}; B NPV {npv(WACC, Bp):.2f} IRR {irr_b:.2%}",
)
M = [-100.0, 230.0, -132.0]
roots = sorted(brentq(lambda r: npv(r, M), a, b) for a, b in ((0.05, 0.15), (0.15, 0.30)))
ok(
    "two sign changes give two IRRs, 10% and 20%; NPV at 8% is -0.21, so reject despite 'IRR > 8%'",
    [round(x, 6) for x in roots] == [0.1, 0.2] and round(npv(WACC, M), 2) == -0.21,
)

# Capital rationing: profitability index against the best combination.
projects = {
    "P1": (115.0, p_npv),
    "P2": (60.0, 9.0),
    "P3": (50.0, 8.0),
    "P4": (40.0, 7.5),
    "P5": (30.0, 3.0),
}
budget = 150.0
order = sorted(projects, key=lambda k: projects[k][1] / projects[k][0], reverse=True)
spent, greedy = 0.0, []
for k in order:
    if spent + projects[k][0] <= budget:
        greedy.append(k)
        spent += projects[k][0]
best = max(
    (
        c
        for n in range(1, 6)
        for c in itertools.combinations(projects, n)
        if sum(projects[k][0] for k in c) <= budget
    ),
    key=lambda c: sum(projects[k][1] for k in c),
)
g_npv, b_npv = sum(projects[k][1] for k in greedy), sum(projects[k][1] for k in best)
ok(
    "budget 150: ranking by PI (P4, P3, P2, P1, P5) and filling greedily gives P4, P3, P2 (NPV 24.50), "
    "which brute-force search confirms is best",
    order == ["P4", "P3", "P2", "P1", "P5"]
    and greedy == ["P4", "P3", "P2"]
    and round(g_npv, 2) == 24.5
    and close(g_npv, b_npv),
    f"greedy {greedy} NPV {g_npv:.2f}; best {list(best)} NPV {b_npv:.2f}",
)
budget2 = 145.0
spent, greedy2 = 0.0, []
for k in order:
    if spent + projects[k][0] <= budget2:
        greedy2.append(k)
        spent += projects[k][0]
best2 = max(
    (
        c
        for n in range(1, 6)
        for c in itertools.combinations(projects, n)
        if sum(projects[k][0] for k in c) <= budget2
    ),
    key=lambda c: sum(projects[k][1] for k in c),
)
g2, b2 = sum(projects[k][1] for k in greedy2), sum(projects[k][1] for k in best2)
ok(
    "budget 145: greedy PI takes P4, P3, P5 (NPV 18.50, 25 idle); search finds P2, P3, P5 (NPV 20.00)",
    greedy2 == ["P4", "P3", "P5"]
    and round(g2, 2) == 18.5
    and sorted(best2) == ["P2", "P3", "P5"]
    and close(b2, 20.0),
    f"greedy {greedy2} NPV {g2:.2f}; best {list(best2)} NPV {b2:.2f}",
)


# Unequal lives: equivalent annual cost.
def annuity(r, n):
    return (1 - (1 + r) ** -n) / r


X = 60 + 10 * annuity(WACC, 3)
Y = 90 + 8 * annuity(WACC, 5)
eac_x, eac_y = X / annuity(WACC, 3), Y / annuity(WACC, 5)
ok(
    "machine X (60, 3 years, 10 a year) vs Y (90, 5 years, 8 a year): PV costs 85.77 vs 121.94, "
    "but equivalent annual cost 33.28 vs 30.54, so Y",
    round(X, 2) == 85.77
    and round(Y, 2) == 121.94
    and round(eac_x, 2) == 33.28
    and round(eac_y, 2) == 30.54,
)
# Replication over 15 years gives the same ranking.
rep_x = sum(X / (1.08 ** (3 * k)) for k in range(5))
rep_y = sum(Y / (1.08 ** (5 * k)) for k in range(3))
ok(
    "replicating both chains over 15 years gives the same choice",
    rep_y < rep_x and close(rep_x / rep_y, eac_x / eac_y, 1e-12),
)

# Real options: a staged expansion valued with a decision tree.
phase1 = -5.0
up, down, cost2, p = 150.0, 80.0, 120.0, 0.5
with_option = phase1 + (p * max(up - cost2, 0) + (1 - p) * max(down - cost2, 0)) / 1.08**2
committed = phase1 + (p * up + (1 - p) * down - cost2) / 1.08**2
ok(
    "expansion option: committing now to both phases gives -9.29; keeping the choice gives +7.86",
    round(committed, 2) == -9.29 and round(with_option, 2) == 7.86,
)

# ---------------------------------------------------------------------------------------------
print("== part 9: Harbour's WACC with market-value weights")
rf, erp, beta_u, kd_pre = 0.03, 0.055, 0.93, 0.052
debt = -(B25["term_loan"] + B25["revolver"] + B25["lease_liab"])
# Claim definitions (corrected 2026-10-20): the 5m vested options are an equity claim, valued here at the
# market price with the inputs of the Harbour equity bridge (strike 8, three years, volatility 30%, rate 3%,
# dividend yield 2.5%), so market equity is shares plus options, as the entry's own definition says.
opt_mkt = 5.0 * H["bs_call"](PRICE, 8.0, 3.0, 0.03, 0.30, 0.025)
mkt_shares = PRICE * SHARES
mkt_eq = mkt_shares + opt_mkt
de = debt / mkt_eq
beta_l = beta_u * (1 + (1 - TAX) * de)
ke = rf + beta_l * erp
kd = kd_pre * (1 - TAX)
w_e, w_d = mkt_eq / (mkt_eq + debt), debt / (mkt_eq + debt)
wacc_mkt = w_e * ke + w_d * kd
ok(
    "options at the market price: 5m x 3.5878 = 17.94; market equity 1,108.25 + 17.94 = 1,126.19",
    round(opt_mkt, 2) == 17.94 and round(mkt_eq, 2) == 1126.19,
)
ok(
    "debt 355 (term loan 250, RCF 40, leases 65), equity incl. options 1,126.19; D/E 31.52%, levered beta "
    "1.1499, ke 9.32%, after-tax kd 3.90%, WACC 8.02%",
    close(debt, 355)
    and round(de, 4) == 0.3152
    and round(beta_l, 4) == 1.1499
    and round(ke, 4) == 0.0932
    and round(wacc_mkt, 4) == 0.0802,
    f"weights E {w_e:.4f} D {w_d:.4f}",
)
de_sup = debt / mkt_shares
ke_sup = rf + beta_u * (1 + (1 - TAX) * de_sup) * erp
wacc_sup = (mkt_shares * ke_sup + debt * kd) / (mkt_shares + debt)
ok(
    "the superseded shares-only weights gave ke 9.34% and WACC 8.02%: the option claim moves ke by 0.02 points "
    "and leaves the WACC unchanged at two decimals",
    round(ke_sup, 4) == 0.0934 and round(wacc_sup, 4) == 0.0802 and abs(wacc_sup - wacc_mkt) < 2e-5,
    f"ke {ke_sup:.5f} -> {ke:.5f}; WACC {wacc_sup:.5f} -> {wacc_mkt:.5f}",
)
book_eq = H["bs_view"](2025)["eq"]
w_book = debt / (debt + book_eq)
wacc_book = (1 - w_book) * ke + w_book * kd
ok(
    "book weights (equity 647.38) put debt at 35.42% and give 7.40%, understating the market-value WACC",
    round(book_eq, 2) == 647.38 and round(w_book, 4) == 0.3542 and round(wacc_book, 4) == 0.0740,
)
wacc_rate_up = w_e * (ke + 0.01) + w_d * (kd_pre + 0.01) * (1 - TAX)
ok(
    "a one-point rise in the risk-free rate (spreads, beta and weights unchanged) adds 0.94 points",
    round(wacc_rate_up - wacc_mkt, 4) == 0.0094,
)
pension_after_tax = -B25["db_liab"] * (1 - TAX)
d_p = debt + pension_after_tax
ke_p = rf + beta_u * (1 + (1 - TAX) * d_p / mkt_eq) * erp
wacc_p = (mkt_eq * ke_p + d_p * kd) / (mkt_eq + d_p)
ok(
    "the after-tax pension deficit 36.12 is a debt-like claim in the bridge; counted as debt at the after-tax "
    "cost of debt it would give WACC 8.02% (8.017% against 8.024%)",
    round(pension_after_tax, 2) == 36.12 and round(wacc_p, 4) == 0.0802 and wacc_p < wacc_mkt,
    f"{wacc_p:.5f}",
)

# ---------------------------------------------------------------------------------------------
print("== part 10: Modigliani-Miller and the trade-off between tax shields and distress costs")
ebit_mm, rho, kd_mm, D_mm = 100.0, 0.10, 0.05, 400.0
V_nt = ebit_mm / rho
E_nt = V_nt - D_mm
ke_nt = (ebit_mm - kd_mm * D_mm) / E_nt
ok(
    "no taxes: V = 1,000 whatever the debt; with D = 400, ke = 13.33% = rho + (rho - kd) D/E and WACC = 10%",
    close(ke_nt, rho + (rho - kd_mm) * D_mm / E_nt)
    and close((ke_nt * E_nt + kd_mm * D_mm) / V_nt, rho),
)
alpha = 0.10
lev_income = alpha * (ebit_mm - kd_mm * D_mm)
home_income = alpha * ebit_mm - kd_mm * alpha * D_mm
ok(
    "homemade leverage: 10% of the unlevered firm plus personal borrowing of 40 pays 8 and costs 60, as 10% of levered equity",
    close(lev_income, home_income) and close(alpha * E_nt, alpha * V_nt - alpha * D_mm),
)
V_u = ebit_mm * (1 - TAX) / rho
V_l = V_u + TAX * D_mm
E_l = V_l - D_mm
ke_l = (ebit_mm - kd_mm * D_mm) * (1 - TAX) / E_l
wacc_l = ke_l * E_l / V_l + kd_mm * (1 - TAX) * D_mm / V_l
ok(
    "corporate tax 25%: V_U 750, V_L = 750 + 0.25 x 400 = 850; ke 13.33% = rho + (rho - kd)(1 - t)D/E; WACC 8.82%",
    close(V_l, 850)
    and close(ke_l, rho + (rho - kd_mm) * (1 - TAX) * D_mm / E_l)
    and round(wacc_l, 4) == 0.0882
    and close(wacc_l, ebit_mm * (1 - TAX) / V_l),
)


def v_tradeoff(D):
    return V_u + TAX * D - 200.0 * (D / V_u) ** 2


grid = np.linspace(0, 750, 75001)
D_star_grid = grid[np.argmax([v_tradeoff(x) for x in grid])]
D_star = TAX * V_u**2 / 400.0
ok(
    "with PV distress costs 200 (D/V_U)^2, value peaks at D = 351.56 (grid and first-order condition agree), "
    "V = 793.95",
    abs(D_star_grid - D_star) < 0.02
    and round(D_star, 2) == 351.56
    and round(v_tradeoff(D_star), 2) == 793.95,
)

# ---------------------------------------------------------------------------------------------
print("== part 11: costs of debt and equity - methods compared")
cpn, years, price_bond = 4.0, 5, 94.83
ytm = brentq(
    lambda y: (
        sum(cpn / (1 + y) ** t for t in range(1, years + 1)) + 100 / (1 + y) ** years - price_bond
    ),
    0,
    1,
)
ok("a 4% five-year bond at 94.83 yields 5.20%", round(ytm, 4) == 0.052)
SPREADS = [  # interest cover lower bound -> (rating, spread): illustrative, calibrated so Harbour maps to 5.2%
    (12.5, "AAA", 0.007),
    (9.5, "AA", 0.009),
    (8.0, "A+", 0.012),
    (7.0, "A", 0.015),
    (6.5, "A-", 0.018),
    (5.5, "BBB", 0.022),
    (4.5, "BB+", 0.030),
    (3.5, "BB", 0.038),
    (3.0, "B+", 0.048),
    (2.5, "B", 0.060),
    (2.0, "B-", 0.075),
    (1.5, "CCC", 0.095),
    (1.0, "CC", 0.120),
    (0.5, "C", 0.150),
    (-1e9, "D", 0.180),
]


def synthetic(cover):
    for lo, rating, spread in SPREADS:
        if cover >= lo:
            return rating, spread


ebit_norm = 111.0  # 2025 operating profit 93 before the 18 restructuring charge
int_2025 = 0.052 * 355
rating, spread = synthetic(ebit_norm / int_2025)
ok(
    "synthetic rating: normalised EBIT 111 over interest at 5.2% on 355 (18.46) = cover 6.01 -> BBB, spread 2.2%, "
    "so rf 3% + 2.2% reproduces the 5.2% bond yield; the 2025 book rate (interest / average debt) is lower",
    round(ebit_norm / int_2025, 2) == 6.01 and rating == "BBB" and close(spread, 0.022),
)
idx_yield, g_long = 0.042, 0.04
implied_r = idx_yield + g_long
ok(
    "implied ERP: cash yield 4.2% + growth 4.0% = 8.2%; less rf 4.0% gives 4.2%",
    close(implied_r - 0.04, 0.042),
)
ff3 = 0.03 + 1.10 * 0.055 + 0.30 * 0.02 + 0.20 * 0.03
build_up = 0.03 + 0.055 + 0.02 + 0.01
bond_plus = kd_pre + 0.04
ok(
    "Harbour ke by method: CAPM 9.32%, three-factor 10.25%, build-up 11.50%, bond yield plus 4% = 9.20%",
    [round(x, 4) for x in (ke, ff3, build_up, bond_plus)] == [0.0932, 0.1025, 0.115, 0.092],
)
beta_kestrel = beta_u * (1 + (1 - TAX) * 0.5)
total_beta = beta_kestrel / 0.45
ok(
    "private Kestrel (D/E 50%): market beta 1.2788; total beta 2.8417 at correlation 0.45; ke 10.03% vs 18.63%",
    round(beta_kestrel, 4) == 1.2788
    and round(total_beta, 4) == 2.8417
    and round(rf + beta_kestrel * erp, 4) == 0.1003
    and round(rf + total_beta * erp, 4) == 0.1863,
)

# ---------------------------------------------------------------------------------------------
print("== part 12: Harbour's cost-of-capital curve and peer comparison")
V_firm = mkt_eq + debt
ebit_2026 = 111.0  # normalised 2025 operating profit, as in the synthetic rating


def kd_fixed_point(D, ebit):
    """Best rating whose own interest charge still earns that rating (the schedule is discrete)."""
    if D == 0:
        return rf + SPREADS[0][2], SPREADS[0][1]
    for lo, rating, spread in SPREADS:
        if ebit / ((rf + spread) * D) >= lo:
            return rf + spread, rating
    return rf + SPREADS[-1][2], SPREADS[-1][1]


def wacc_at(dv, ebit=ebit_2026):
    D = dv * V_firm
    E = V_firm - D
    kd_try, _ = kd_fixed_point(D, ebit)
    b = beta_u * (1 + (1 - TAX) * D / E)
    return E / V_firm * (rf + b * erp) + D / V_firm * kd_try * (1 - TAX), kd_try


curve = {dv: wacc_at(dv) for dv in np.round(np.arange(0.0, 0.71, 0.05), 2)}
best_dv = min(curve, key=lambda k: curve[k][0])
ok(
    "illustrative schedule (firm value 1,481.19 incl. options): WACC 8.12% unlevered, lowest 7.84% at 20% debt, "
    "8.02% at 25% (Harbour's rating), then rising as the rating falls: 8.36% at 30%, 10.90% at 40%",
    best_dv == 0.2
    and [round(curve[k][0], 4) for k in (0.0, 0.2, 0.25, 0.3, 0.4, 0.5)]
    == [0.0812, 0.0784, 0.0802, 0.0836, 0.109, 0.1273]
    and [round(curve[k][1], 3) for k in (0.0, 0.2, 0.25, 0.3, 0.4, 0.5)]
    == [0.037, 0.039, 0.052, 0.068, 0.15, 0.18]
    and round(V_firm, 2) == 1481.19,
    ", ".join(f"{k:.0%}: {v[0]:.2%} (kd {v[1]:.1%})" for k, v in curve.items()),
)
lev_at = {dv: (dv * V_firm - B25["cash"]) / R25["ebitda"] for dv in (0.2, 0.3, 0.35)}
ok(
    "the 2.50x leverage covenant binds just above 35% debt: net debt/EBITDA 1.33 at 20%, 2.09 at 30%, 2.47 at 35%",
    [round(v, 2) for v in lev_at.values()] == [1.33, 2.09, 2.47],
)
peers_dv = np.array([0.18, 0.22, 0.28, 0.31, 0.35])
ok(
    "peer median debt/value 28% against Harbour's 23.97%",
    close(np.median(peers_dv), 0.28) and round(w_d, 4) == 0.2397,
)

# ---------------------------------------------------------------------------------------------
print("== part 13: distributions - stock dividends, splits and buybacks")
n0, p0 = SHARES, PRICE
ok(
    "10% stock dividend: 110.825m shares at 10.00, value 1,108.25 unchanged; 2-for-1 split: 201.5m at 5.50",
    close(n0 * 1.1 * p0 / 1.1, n0 * p0)
    and close(round(n0 * 1.1, 3), 110.825)
    and close(p0 / 2, 5.5),
)
NI_r, N_r, P_r, BV_r = 80.0, 100.0, 16.0, 400.0
buy = 0.10 * N_r * P_r
eps0 = NI_r / N_r
results = {}
for label, after_tax_cost in (
    ("cash earning 2%", 0.02),
    ("debt at 4%", 0.04),
    ("debt at 6%", 0.06),
):
    results[label] = (NI_r - buy * after_tax_cost) / (N_r * 0.9)
ok(
    "buyback of 10% at 16 (cost 160): EPS 0.80 -> 0.8533 (cash), 0.8178 (debt 4%), 0.7822 (debt 6%)",
    [round(v, 4) for v in results.values()] == [0.8533, 0.8178, 0.7822],
)
ok(
    "rule: EPS rises if and only if the after-tax cost of funds is below the earnings yield 5%",
    all(
        (v > eps0) == (c < NI_r / (N_r * P_r)) for v, c in zip(results.values(), (0.02, 0.04, 0.06))
    ),
)
ok(
    "BVPS 4.00 -> 2.67 when buying at 16 above book; buying at 3 (below book) would raise it to 4.11",
    round((BV_r - buy) / 90, 4) == 2.6667 and round((BV_r - 30) / 90, 4) == 4.1111,
)
ok(
    "the buyback leaves value per share unchanged at a fair price: (1,600 - 160)/90 = 16",
    close((N_r * P_r - buy) / 90, P_r),
)

# ---------------------------------------------------------------------------------------------
print("== part 14: dividend taxes and payout policies")
eff_double = 1 - (1 - 0.25) * (1 - 0.30)
grossed = 100.0
imput_personal = 0.45 * grossed - 30.0
ok(
    "double taxation 25% then 30% on dividends: 47.5%; full imputation (corporate 30%, personal 45%): "
    "shareholder pays 15 more, total 45%",
    close(eff_double, 0.475) and close(imput_personal, 15) and close(30 + imput_personal, 45),
)
split_rate = 1 - (1 - 0.20) * (1 - 0.30)
ok("split rate: distributed profit taxed at 20% then 30% bears 44%", close(split_rate, 0.44))
eps_path = [2.00, 2.50, 1.80, 2.60, 2.90]
target, speed, d_prev = 0.40, 0.5, 0.70
lintner, constant = [], []
for e in eps_path:
    d_prev = d_prev + speed * (target * e - d_prev)
    lintner.append(d_prev)
    constant.append(target * e)
closed = []
for t in range(len(eps_path)):
    val = (1 - speed) ** (t + 1) * 0.70 + sum(
        speed * (1 - speed) ** (t - j) * target * eps_path[j] for j in range(t + 1)
    )
    closed.append(val)
ok(
    "Lintner (target 40%, speed 0.5) by recursion equals the weighted-average closed form",
    all(close(a, b, 1e-12) for a, b in zip(lintner, closed)),
    "Lintner "
    + ", ".join(f"{x:.4f}" for x in lintner)
    + "; constant payout "
    + ", ".join(f"{x:.2f}" for x in constant),
)
ok(
    "smoothing: standard deviation of dividend changes 0.0779 (Lintner) against 0.2014 (constant payout)",
    round(np.std(np.diff([0.70, *lintner])), 4) == 0.0779
    and round(np.std(np.diff([0.70, *constant])), 4) == 0.2014,
)

# ---------------------------------------------------------------------------------------------
print("== part 15: dividend coverage and sustainability")
profit25, divs25 = 55.38, 32.0
fcfe25 = H["fcfe"]
t25 = H["t25"]
issue25 = t25[("fin", "share_issue")]
dcash25 = B25["cash"] - H["B"][2024]["cash"]
ok(
    "Harbour 2025: earnings cover 1.73x, payout 57.8%; FCFE 28.04 covers dividends 0.88x",
    round(profit25 / divs25, 2) == 1.73
    and round(divs25 / profit25, 3) == 0.578
    and round(fcfe25 / divs25, 2) == 0.88,
)
ok(
    "statutory FCFE reconciliation (corrected): FCFE 28.04 = dividends 32 - equity-issue proceeds 6 + cash "
    "increase 2.04; omitting the issue proceeds would leave a gap of 6",
    close(fcfe25, divs25 - issue25 + dcash25, 1e-9)
    and close(issue25, 6.0)
    and round(dcash25, 2) == 2.04
    and round(divs25 + dcash25 - fcfe25, 2) == 6.0,
)
fcfe_val25 = H["fcfe_val25"]
ok(
    "on the valuation convention (share-based pay of 9 charged as a cost) FCFE is 19.04, cover 0.595x",
    round(fcfe_val25, 2) == 19.04 and round(fcfe_val25 / divs25, 3) == 0.595,
)
f26 = H["base"][0]
ok(
    "2026 forecast: profit 73.40, dividends 29.36 (40% payout), earnings cover 2.5x",
    round(f26["profit"], 2) == 73.4
    and round(f26["divs"], 2) == 29.36
    and round(f26["profit"] / f26["divs"], 2) == 2.5,
)
# Ridgeway (corrected 2026-10-20). FCFE already contains actual net borrowing, so the dividend-FCFE gap
# cannot be "funded by borrowing" again. Each year: free cash flow before net borrowing (CFO after interest
# less net capital spending), actual net borrowing, FCFE, dividends, no share issues or buybacks, and cash.
ridge = dict(
    ni=[120.0, 100.0, 85.0],
    div=[110.0, 112.0, 114.0],
    fcf_pre=[60.0, 52.0, 34.0],
    borrow=[30.0, 18.0, 21.0],
    ebitda=[400.0, 380.0, 360.0],
)
ridge_debt0, ridge_cash0, ridge_ebitda0 = 1050.0, 200.0, 400.0
ridge["fcfe"] = [a + b for a, b in zip(ridge["fcf_pre"], ridge["borrow"])]
debt_t, cash_t = [], []
dbt, csh = ridge_debt0, ridge_cash0
for fc, bo, dv in zip(ridge["fcfe"], ridge["borrow"], ridge["div"]):
    dbt += bo
    csh += fc - dv  # the cash identity: FCFE - dividends (no issues or buybacks) = change in cash
    debt_t.append(dbt)
    cash_t.append(csh)
ridge["net_debt"] = [d - c for d, c in zip(debt_t, cash_t)]
payout = [d / n for d, n in zip(ridge["div"], ridge["ni"])]
fc = [f / d for f, d in zip(ridge["fcfe"], ridge["div"])]
lev = [n / e for n, e in zip(ridge["net_debt"], ridge["ebitda"])]
ok(
    "Ridgeway: FCFE 90, 70, 55 = FCF before borrowing 60, 52, 34 + actual net borrowing 30, 18, 21; net debt "
    "900, 960, 1,040",
    ridge["fcfe"] == [90.0, 70.0, 55.0] and ridge["net_debt"] == [900.0, 960.0, 1040.0],
    f"debt {debt_t}, cash {cash_t}",
)
ok(
    "payout 92% -> 134%, FCFE cover 0.82 -> 0.48, net debt/EBITDA 2.25 -> 2.89",
    round(payout[0], 2) == 0.92
    and round(payout[-1], 2) == 1.34
    and round(fc[0], 2) == 0.82
    and round(fc[-1], 2) == 0.48
    and round(lev[0], 2) == 2.25
    and round(lev[-1], 2) == 2.89,
)
gap = sum(ridge["div"]) - sum(ridge["fcfe"])
ok(
    "dividends exceed FCFE by 121 over three years, met from cash (200 -> 79), not by further borrowing: "
    "actual borrowing 69 is already inside FCFE",
    close(gap, 121.0)
    and close(ridge_cash0 - cash_t[-1], gap)
    and close(sum(ridge["borrow"]), 69.0),
)
ok(
    "net debt rises 190 = borrowing 69 + cash drawn 121 = dividends 336 - FCF before borrowing 146 "
    "(no double count)",
    close(ridge["net_debt"][-1] - (ridge_debt0 - ridge_cash0), 190.0)
    and close(sum(ridge["borrow"]) + gap, 190.0)
    and close(sum(ridge["div"]) - sum(ridge["fcf_pre"]), 190.0),
)
# Target-policy borrowing: holding net debt at 2.25x EBITDA lets net debt change by 2.25 x the change in
# EBITDA (0, -45, -45 as EBITDA falls 400 -> 360). FCFE on that policy = FCF before borrowing + policy borrowing.
policy = [2.25 * (e - p) for e, p in zip(ridge["ebitda"], [ridge_ebitda0, *ridge["ebitda"][:-1]])]
fcfe_policy = [a + b for a, b in zip(ridge["fcf_pre"], policy)]
ok(
    "at a 2.25x net-debt policy the borrowing capacity is 0, -45, -45: policy FCFE 60, 7, -11 (56) against "
    "dividends 336, cover 0.17",
    policy == [0.0, -45.0, -45.0]
    and fcfe_policy == [60.0, 7.0, -11.0]
    and round(sum(fcfe_policy) / sum(ridge["div"]), 2) == 0.17,
)

# ---------------------------------------------------------------------------------------------
print("== part 16: restructuring - the Harbour bolt-on acquisition and a cost programme")
acq = dict(price=60.0, revenue=50.0, ebitda=9.0, intangibles=20.0)
ev_ebitda_paid = acq["price"] / acq["ebitda"]
ok("price 60 for EBITDA 9 is 6.67x", round(ev_ebitda_paid, 2) == 6.67)
comp_co, comp_tx = 7.5, 8.0
ok(
    "comparable companies at 7.5x give 67.5; precedent transactions at 8.0x (control included) give 72.0",
    close(comp_co * acq["ebitda"], 67.5) and close(comp_tx * acq["ebitda"], 72.0),
)
standalone, synergy_pv = 52.0, 14.0
ok(
    "value created 52 + 14 - 60 = 6 for Harbour; the seller receives 8 of the 14 synergy value as premium",
    close(standalone + synergy_pv - acq["price"], 6.0) and close(acq["price"] - standalone, 8.0),
)
net_debt25 = debt - B25["cash"]
pf_lev = (net_debt25 + acq["price"]) / (R25["ebitda"] + acq["ebitda"])
ok(
    "net debt/EBITDA 1.63 -> 1.85 pro forma (full-year target EBITDA, debt-financed price)",
    round(net_debt25 / R25["ebitda"], 2) == 1.63 and round(pf_lev, 2) == 1.85,
)
target_ebit = (
    acq["ebitda"] - 2.0 - acq["intangibles"] / 10
)  # depreciation 2 on PP&E 10 over 5 years
target_ni = (target_ebit - kd_pre * acq["price"]) * (1 - TAX)
eps_base = profit25 / 100.375
eps_pf = (profit25 + target_ni) / 100.375
ok(
    "EPS effect (2025 basis, full year): target EBIT 5.00 less interest 3.12 at 5.2%, after tax 1.41; "
    "EPS 0.5517 -> 0.5658 (+2.5%)",
    close(target_ebit, 5.0)
    and round(target_ni, 2) == 1.41
    and round(eps_base, 4) == 0.5517
    and round(eps_pf, 4) == 0.5658,
)
ok(
    "return on the price (corrected): EBIT/price 8.33% is pre-tax; after tax 5.0 x 0.75 / 60 = 6.25%, "
    "1.77 points below the 8.02% after-tax WACC, although EPS rises",
    round(target_ebit / acq["price"], 4) == 0.0833
    and close(target_ebit * (1 - TAX) / acq["price"], 0.0625)
    and round(wacc_mkt - 0.0625, 4) == 0.0177
    and eps_pf > eps_base,
)
ok(
    "accretion test: EPS rises because the after-tax return 6.25% exceeds the after-tax cost of debt 3.90%, "
    "a test that ignores the equity cost of the risk added",
    0.0625 > kd and close(target_ni, (0.0625 - kd) * acq["price"]),
)
eq_pf = mkt_eq
debt_pf = debt + acq["price"]
de_pf = debt_pf / eq_pf
beta_pf = beta_u * (1 + (1 - TAX) * de_pf)
ke_pf = rf + beta_pf * erp
wacc_pf = eq_pf / (eq_pf + debt_pf) * ke_pf + debt_pf / (eq_pf + debt_pf) * kd
kd_pf, rating_pf = kd_fixed_point(debt_pf, ebit_norm + 5.0)
wacc_pf_rerated = eq_pf / (eq_pf + debt_pf) * ke_pf + debt_pf / (eq_pf + debt_pf) * kd_pf * (
    1 - TAX
)
ok(
    "WACC effect: debt 415 against equity incl. options 1,126.19, D/E 36.85%, beta 1.1870, ke 9.53%; at an "
    "unchanged 5.2% kd WACC is 8.01%, but cover 116/(415 x kd) re-rates the debt to BB+ (6.0%) and WACC is 8.17%",
    round(de_pf, 4) == 0.3685
    and round(beta_pf, 4) == 1.187
    and round(ke_pf, 4) == 0.0953
    and round(wacc_pf, 4) == 0.0801
    and rating_pf == "BB+"
    and round(wacc_pf_rerated, 4) == 0.0817
    and wacc_pf_rerated > wacc_mkt,
    f"re-rated {rating_pf} kd {kd_pf:.2%} WACC {wacc_pf_rerated:.2%}",
)
ok(
    "walk-away price: standalone 52 + synergy 14 = 66, above which all synergy goes to the seller",
    close(standalone + synergy_pv, 66.0),
)
prog_cost, saving, years_s = 12.0, 8.0, 5
prog_npv = -prog_cost + saving * (1 - TAX) * annuity(WACC, years_s)
ok(
    "cost programme: 12 now (deductible, after tax 9) for 8 a year pre-tax for five years: NPV 14.96 on the cash cost",
    round(-prog_cost * (1 - TAX) + saving * (1 - TAX) * annuity(WACC, years_s), 2) == 14.96,
    f"without the deduction on the cost: {prog_npv:.2f}",
)
late = -prog_cost * (1 - TAX) + saving * (1 - TAX) * annuity(WACC, years_s) / (1 + WACC)
half = -prog_cost * (1 - TAX) + 0.5 * saving * (1 - TAX) * annuity(WACC, years_s)
ok(
    "cost programme: savings a year late give NPV 13.18; half the savings give 2.98",
    round(late, 2) == 13.18 and round(half, 2) == 2.98,
    f"{late:.4f}, {half:.4f}",
)
spin_parent, spin_unit, conglomerate = 1200.0, 450.0, 1500.0
ok(
    "a spin-off reveals a 150 (9.1%) discount only if parts trade at 1,650 against 1,500 combined; "
    "dis-synergies of 20 a year after tax at 8% (250) would remove it",
    close(spin_parent + spin_unit - conglomerate, 150)
    and round(150 / 1650, 3) == 0.091
    and close(20 / 0.08, 250),
)

print(f"\n{n_checks} checks executed")
if fails:
    print("FAILED:", fails)
    sys.exit(1)
print("all checks passed")
