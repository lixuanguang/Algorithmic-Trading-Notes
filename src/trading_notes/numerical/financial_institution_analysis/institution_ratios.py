"""Bank capital, asset-quality, earnings and liquidity ratios, and insurer operating ratios."""

from trading_notes.records import Record


class BankRatios(Record):
    """A bank's ratios for one year.

    Attributes:
        cet1: CET1 / RWA.
        tier1: (CET1 + AT1) / RWA.
        total: Total capital / RWA.
        leverage: Tier 1 / leverage exposure.
        npl: Non-performing loans / loans.
        coverage: Allowance / non-performing loans.
        cost_risk: Provisions / loans.
        nim: Net interest income / average earning assets.
        cost_income: Operating expenses / (net interest income + fees).
        roa: Net income / average assets.
        roe: Net income / equity.
        lcr: HQLA / 30-day net outflows.
        nsfr: Available / required stable funding.
        ltd: Loans / deposits.
    """

    cet1: float
    tier1: float
    total: float
    leverage: float
    npl: float
    coverage: float
    cost_risk: float
    nim: float
    cost_income: float
    roa: float
    roe: float
    lcr: float
    nsfr: float
    ltd: float

    def figures(self) -> dict[str, float]:
        """Return the ratios by name, in the order above."""
        return {name: float(value) for name, value in self.model_dump().items()}


class BankAccounts(Record):
    """A bank's capital, balance-sheet, income and liquidity figures for one year.

    Attributes:
        cet1: Common equity Tier 1 capital.
        at1: Additional Tier 1 capital.
        t2: Tier 2 capital.
        rwa: Risk-weighted assets.
        exposure: Leverage exposure.
        loans: Loans.
        npl: Non-performing loans.
        allowance: Loan-loss allowance.
        deposits: Deposits.
        nii: Net interest income.
        fees: Fee income.
        opex: Operating expenses.
        provisions: Loan-loss provisions.
        tax_rate: Tax rate.
        avg_assets: Average assets.
        avg_earning: Average earning assets.
        hqla: High-quality liquid assets.
        outflows30: Net cash outflows over 30 days.
        asf: Available stable funding.
        rsf: Required stable funding.
        equity: Book equity.
    """

    cet1: float
    at1: float
    t2: float
    rwa: float
    exposure: float
    loans: float
    npl: float
    allowance: float
    deposits: float
    nii: float
    fees: float
    opex: float
    provisions: float
    tax_rate: float
    avg_assets: float
    avg_earning: float
    hqla: float
    outflows30: float
    asf: float
    rsf: float
    equity: float

    def pre_tax_income(self) -> float:
        """Return net interest income plus fees, less expenses and provisions."""
        return self.nii + self.fees - self.opex - self.provisions

    def ratios(self) -> BankRatios:
        """Return the year's ratios from their definitions."""
        ni = (self.nii + self.fees - self.opex - self.provisions) * (1 - self.tax_rate)
        return BankRatios(
            cet1=self.cet1 / self.rwa,
            tier1=(self.cet1 + self.at1) / self.rwa,
            total=(self.cet1 + self.at1 + self.t2) / self.rwa,
            leverage=(self.cet1 + self.at1) / self.exposure,
            npl=self.npl / self.loans,
            coverage=self.allowance / self.npl,
            cost_risk=self.provisions / self.loans,
            nim=self.nii / self.avg_earning,
            cost_income=self.opex / (self.nii + self.fees),
            roa=ni / self.avg_assets,
            roe=ni / self.equity,
            lcr=self.hqla / self.outflows30,
            nsfr=self.asf / self.rsf,
            ltd=self.loans / self.deposits,
        )


class InsurerRatios(Record):
    """A non-life insurer's ratios for one year.

    Attributes:
        loss: Losses and loss adjustment expenses / net earned premiums.
        expense: Underwriting expenses / net earned premiums.
        combined: Loss ratio + expense ratio.
        operating: Combined ratio less investment income / net earned premiums.
        yield_: Investment income / invested assets.
        solvency: Own funds / SCR.
        premium_leverage: Net earned premiums / equity.
        development: Reserve development / opening reserves.
    """

    loss: float
    expense: float
    combined: float
    operating: float
    yield_: float
    solvency: float
    premium_leverage: float
    development: float

    def figures(self) -> dict[str, float]:
        """Return the ratios by name, in the order above."""
        return {name: float(value) for name, value in self.model_dump().items()}


class InsurerAccounts(Record):
    """A non-life insurer's underwriting, investment and capital figures for one year.

    Attributes:
        nep: Net earned premiums.
        losses: Incurred losses.
        lae: Loss adjustment expenses.
        uw_exp: Underwriting expenses.
        pol_div: Policyholder dividends.
        inv_inc: Investment income.
        reserves_prior: Opening loss reserves.
        development: Prior-year reserve development (positive is adverse).
        own_funds: Solvency II own funds.
        scr: Solvency capital requirement.
        equity: Book equity.
        invested: Invested assets.
    """

    nep: float
    losses: float
    lae: float
    uw_exp: float
    pol_div: float
    inv_inc: float
    reserves_prior: float
    development: float
    own_funds: float
    scr: float
    equity: float
    invested: float

    def underwriting_result(self) -> float:
        """Return premiums less losses, loss adjustment and underwriting expenses."""
        return self.nep - self.losses - self.lae - self.uw_exp

    def ratios(self) -> InsurerRatios:
        """Return the year's ratios from their definitions."""
        loss_ratio = (self.losses + self.lae) / self.nep
        exp_ratio = self.uw_exp / self.nep
        combined = loss_ratio + exp_ratio
        return InsurerRatios(
            loss=loss_ratio,
            expense=exp_ratio,
            combined=combined,
            operating=combined - self.inv_inc / self.nep,
            yield_=self.inv_inc / self.invested,
            solvency=self.own_funds / self.scr,
            premium_leverage=self.nep / self.equity,
            development=self.development / self.reserves_prior,
        )
