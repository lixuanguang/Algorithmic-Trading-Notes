"""Repo interest and haircuts, a short-term funding comparison and a repo margin call."""

import sys

from trading_notes.numerical.money_markets.money_market_instruments import (
    DiscountPaper,
    Repo,
    RepoMargin,
)
from trading_notes.numerical.report import CheckReport, print_versions
from trading_notes.numerical.tolerance import close


def check_repo_interest(report: CheckReport) -> None:
    """Part 1: repo interest and haircut, the Handbook's worked numbers."""
    print("== part 1: repo interest and haircut (Handbook chap. 60, pp. 1486-1487)")
    full = 10_015_455.0
    repo = Repo(cash=full, rate=0.0008, days=10)
    interest = repo.interest()
    report.ok(
        "10-day repo at 0.08% on 10,015,455: interest 222.57, repurchase price 10,015,677.57",
        abs(interest - 222.57) < 0.005 and abs(repo.repurchase_price() - 10_015_677.57) < 0.005,
        f"{interest:.2f}",
    )
    lent = full / 1.02
    int_h = Repo(cash=lent, rate=0.0008, days=10).interest()
    report.ok(
        "with collateral at 102% of the loan: 9,819,073.53 lent, interest 218.20, repurchase"
        " 9,819,291.73",
        abs(lent - 9_819_073.53) < 0.005
        and abs(int_h - 218.20) < 0.005
        and abs(lent + int_h - 9_819_291.73) < 0.01,
    )
    report.ok(
        "haircut as a share of collateral value is 1 - 1/1.02 = 1.96%, not 2%",
        abs((full - lent) / full - 0.0196078) < 1e-6,
    )


def check_funding_comparison(report: CheckReport) -> None:
    """Part 2: an original 90-day funding comparison for 20 million at illustrative rates."""
    print("== part 2: original 90-day funding comparison for 20 million (illustrative rates)")
    need, days = 20_000_000.0, 90
    yf = days / 360
    # (a) commercial paper: discount rate 4.40% on 20m face; dealer fee 5 bp a year on face; backup
    # line of 25m at 10 bp
    d_cp = 0.0440
    cp = DiscountPaper(discount_rate=d_cp, days=days)
    face = cp.face_for(need)  # issue enough face to raise exactly 20m
    proceeds = face * (1 - d_cp * yf)
    cp_interest = face - need
    cp_fees = face * 0.0005 * yf + 25_000_000 * 0.0010 * yf
    cp_cost = (cp_interest + cp_fees) / need / yf
    mmy = cp.money_market_yield()
    report.ok(
        "CP: face 20,222,446.92 raises 20m; the 4.40% discount rate is a 4.4489% money-market"
        " yield, equal to interest"
        " over proceeds annualised on act/360",
        abs(face - 20_222_446.92) < 0.01
        and abs(mmy - 0.044489) < 1e-6
        and close(cp_interest / need / yf, mmy, 1e-12)
        and close(proceeds, need, 1e-6),
        f"{face:,.2f}",
    )
    # (b) revolver: 30m committed, 20m drawn at expected SOFR 4.20% + 125 bp; 20 bp commitment fee
    # on the undrawn 10m
    rev_interest = need * (0.0420 + 0.0125) * yf
    rev_fee = 10_000_000 * 0.0020 * yf
    rev_cost = (rev_interest + rev_fee) / need / yf
    # (c) repo: Treasury collateral, 2% haircut on market value, repo rate 4.25% (term, 90 days)
    repo_rate = 0.0425
    collateral = need / 0.98
    repo_cost = repo_rate
    report.ok(
        "all-in annual costs: CP 4.6245% (yield 4.4489% + dealer fee 5.06 bp + backup line 12.5"
        " bp), revolver 5.550%,"
        " repo 4.250% (on 20.41m of collateral)",
        abs(cp_cost - 0.046245) < 1e-6
        and close(cp_cost, mmy + face / need * 0.0005 + 25 / 20 * 0.0010, 1e-12)
        and abs(rev_cost - 0.0555) < 1e-12
        and abs(collateral - 20_408_163.27) < 0.01,
        f"CP {cp_cost:.6f}, revolver {rev_cost:.6f}",
    )
    report.ok(
        "ranking repo < CP < revolver, but CP needs a backup line and repo needs unencumbered"
        " collateral",
        repo_cost < cp_cost < rev_cost,
    )
    # rollover stress: CP cannot be rolled for the last 30 days; the backup line is drawn at SOFR +
    # 125 bp
    cp_stressed = (
        (
            need * mmy * 60 / 360
            + need * (0.0420 + 0.0125) * 30 / 360
            + face * 0.0005 * 60 / 360
            + 25_000_000 * 0.0010 * yf
        )
        / need
        / yf
    )
    report.ok(
        "if CP cannot roll for the last 30 days and the backup line is drawn, the all-in cost"
        " rises to 4.9413%",
        abs(cp_stressed - 0.049413) < 1e-6 and cp_cost < cp_stressed < rev_cost,
        f"{cp_stressed:.6f}",
    )


def check_margin_call(report: CheckReport) -> None:
    """Part 3: a repo margin call after a collateral fall, and the lender's exposure."""
    print("== part 3: repo margin call and the lender's exposure")
    mv0, loan = 51_020_408.16, 50_000_000.0  # 2% haircut on market value
    margin = RepoMargin(loan=loan, loan_to_value=0.98)
    report.ok(
        "a 50m repo against 51.02m of collateral has a 2% haircut on market value",
        abs(loan / mv0 - 0.98) < 1e-9,
    )
    mv1 = mv0 * 0.97  # collateral falls 3%
    deficit = margin.deficit(mv1)
    report.ok(
        "after a 3% fall the collateral is 49.49m against 51.02m required: margin deficit 1.53m",
        abs(mv1 - 49_489_795.92) < 0.01 and abs(deficit - 1_530_612.24) < 0.01,
    )
    report.ok(
        "without the call the lender is under-collateralised by 0.51m (loan above collateral)",
        abs(loan - mv1 - 510_204.08) < 0.01,
    )
    cash_cure = deficit
    reduce_loan = margin.cash_repayment(mv1)
    report.ok(
        "the borrower cures by posting 1.53m of securities or by repaying 1.50m of cash, which"
        " restores the 2% haircut",
        abs(reduce_loan - 1_500_000.0) < 0.01
        and close((loan - reduce_loan) / mv1, 0.98, 1e-12)
        and cash_cure > reduce_loan,
    )


def main() -> int:
    """Run every check with a fresh report, print the summary and return the exit status (0 or 1).

    Reproduced from Fabozzi (ed.), Handbook of Fixed Income Securities, 9th ed. (2021), chap. 60
    (Fabozzi and Mann), pp. 1486-1487: dollar interest on a 10-day term repo at 0.08 percent and
    the same repo with a 2 percent haircut. Everything else is an original example with
    invented, illustrative rates (not market quotes for any date): a company that needs
    20 million for 90 days compares commercial paper with a backup line, a drawn revolving credit
    facility and a repo on Treasury collateral; a repo margin call after a collateral fall.
    Money-market conventions: act/360 simple interest; commercial paper quoted on a discount
    basis. One check is one executed ok() call (a call inside a loop counts once per iteration).
    """
    print_versions()
    report = CheckReport()
    check_repo_interest(report)
    check_funding_comparison(report)
    check_margin_call(report)
    print()
    if report.failures:
        print(f"{len(report.failures)} check(s) failed: {report.failures}")
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
