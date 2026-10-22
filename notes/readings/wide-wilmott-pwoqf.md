---
key: wide-wilmott-pwoqf
pathways: [stochastic-processes-calculus, volatility-options, option-pricing-models, portfolio-construction, rates-credit-mortgages, risk-tail-systemic]
version: Paul Wilmott, Paul Wilmott on Quantitative Finance, 2nd ed., John Wiley & Sons, Chichester, 2006, three volumes in one PDF (ISBN 978-0-470-01870-5, copyright page). Matches the catalogue entry (second edition, 2006, three-volume set, ISBN 9780470018705). Copy used: the owner's library, `CQF-1-master/Textbooks/Paul Wilmott on Quantitative Finance Vol 1-3, 2nd Ed.pdf` (read-only; SHA-256 e0ff5f09420bc38876b056d6a5e746bf0020b09fd89672bbf7066486feffd549), 1,401 PDF pages with a text layer; printed page = PDF page - 21 throughout volume 1 (checked at pp. 72, 179 and 306) and at the volume-3 pages cited (pp. 1214, 1227). Volume and page are cited as printed; the book's index uses "volume:page".
sections: library gap-filling Batch L1 (2026-10-21): contents; chap. 4, secs. 4.2-4.14, pp. 71-88 (coin-tossing walk, Markov and martingale properties, quadratic variation, Brownian motion and its properties, stochastic integration, the mean-square limit, Itô's lemma by Taylor series and the dX^2 = dt rule, Itô in two dimensions, the lognormal walk and its solution); chap. 10, secs. 10.11-10.12, pp. 179-181 (backward Kolmogorov equation, present value of an expected payoff, the risk-neutral random walk, delta is not the probability of exercise); P2: chap. 77, secs. 77.11-77.12 and 77.17, pp. 1212-1215 and 1224-1226 (explicit coefficients, stability conditions, upwinding); chap. 78, secs. 78.1-78.3, 78.7 and 78.9, pp. 1227-1230, 1242-1246 (implicit and Crank-Nicolson schemes, three-level schemes, early exercise by projection and projected SOR, Bermudan payoffs); chap. 80, secs. 80.1-80.6, pp. 1263-1269 (Monte Carlo pricing, Euler and exact lognormal stepping, the O(dt) against O(N^-1/2) error balance); P3: chap. 2, pp. 43-44 (binary payoffs and binary put-call parity); chap. 7, pp. 119-121 (binary call and put values); chap. 23, secs. 23.1-23.2 and 23.6-23.8, pp. 385-386 and 400-405 (barrier types, first-exit time, volatility choice, hedging through the barrier); chap. 25, secs. 25.9-25.11, pp. 440-442 (closed forms and approximations, term-structure effects, geometric average-rate formulas; p. 440 page image viewed); P4: chap. 7, pp. 127-128 and n. 3 (vega, vomma and kabanga); chap. 12, pp. 197-205 (how to delta hedge: implied against actual volatility, both cases, eq. (12.2), expected profit of the implied hedge); chap. 47, pp. 763-770 (discrete hedging, the hedging error); P5: chap. 17, sec. 17.5, pp. 306-309 (the Kelly criterion, eqs. (17.1)-(17.2)); chap. 66, sec. 66.4, pp. 1057-1058 (maximising long-term growth, logarithmic bequest function); library gap-filling Batch L2 (2026-10-21): P6, chap. 30, secs. 30.6-30.8, pp. 515-520 (the general affine model and why it is the most general with exponential-affine bond prices, constant-parameter solution, steady-state density, Vasicek and CIR, CIR positivity when eta > alpha/2); chap. 31, pp. 525-531 (yield-curve fitting: Ho-Lee and extended Vasicek fitted drifts, eqs. (31.1)-(31.3), the case for and against fitting, refitted drifts, BDT and Black-Karasinski); chap. 37, secs. 37.1-37.13, pp. 609-619 (HJM forward-rate equation, the spot-rate process and its non-Markov nature, market price of risk, the risk-neutral drift eq. (37.4), simulation, trees, Musiela parameterisation, multi-factor HJM, Ho-Lee as HJM, principal components); P9, chap. 19, secs. 19.6-19.8.1, pp. 338-341 (bootstrap VaR, VaR as a performance measure, introductory EVT: maxima and peaks over threshold); library gap-filling Batch L5 (2026-10-21): L5-a, chap. 24, secs. 24.4-24.5, pp. 422-425 (updating rules for an average and a maximum, jump condition (24.5), the discrete-sampling algorithm) and chap. 26, pp. 445-452 (payoff types; continuous maximum with dM = 0 below it and dV/dM = 0 on S = M; discrete measurement and its jump condition; similarity reduction (26.1); sec. 26.6 floating and fixed-strike formulas; further reading); L5-b, chap. 48, secs. 48.1-48.14 and appendix, pp. 783-811 (the effect of costs; Leland's model and adjusted volatilities; the Hoggard-Whalley-Wilmott derivation (48.1)-(48.6) and nonlinearity; K (48.7) and ill-posedness; non-single-signed gamma; the marginal effect; other cost structures (48.8); the bandwidth (48.9)-(48.10); utility models and the asymptotic band; negative prices; existence; non-normal returns, Table 48.1; Jefferies' empirical tests; costs against hedging error; the appendix derivation), pp. 785, 788 and 789 also viewed as page images; pre-L5 audit (C1-F2), chap. 10, secs. 10.2-10.6, pp. 169-175 (transition density, trinomial walk, forward equation (10.2) on p. 172, lognormal solution (10.3), steady state, backward equation (10.4) on p. 175)
read:
status: draft
---

Prepared on 2026-10-21 by library gap-filling Batch L1 from source checks, not from study: the headings that need your own reading are left empty. Used for `def:brownian-motion-quadratic-variation`, `res:ito-lemma-geometric-brownian-motion` and `res:risk-neutral-pricing-feynman-kac`.


Also used by library gap-filling Batch L2 (2026-10-21) for `mod:affine-short-rate-models`, `mod:hjm-forward-rate-models` and the extension of `mod:term-structure-models-simulation` (`rates-credit-mortgages`).


Also used for `meth:extreme-value-tail-estimation` (`risk-tail-systemic`).


Also used by library gap-filling Batch L5 (2026-10-21) for `meth:lookback-option-valuation` and `meth:transaction-cost-hedging` (`volatility-options`).

## Question and claim

## Mechanism

## Method

## Data and timing

## Key results

- Quadratic variation of the scaled walk equals elapsed time; Brownian motion is finite, continuous, Markov, a martingale, has normal increments and quadratic variation $t$ (pp. 73-75).
- Stochastic integrals evaluate the integrand at the left point: non-anticipatory, "we take some action ... and only then does the stock price move" (pp. 75-76).
- $E[(\sum(\Delta X)^2-t)^2]=O(1/n)$, so $\int_0^t(dX)^2=t$ in the mean-square limit (pp. 77-78).
- Itô's lemma $dF=F'dX+\tfrac12F''dt$; for $F=X^2$, $\int_0^tX\,dX=\tfrac12X^2-\tfrac12t$ (pp. 78-80). Rule of thumb $dX^2=dt$, "technically incorrect" but gives the right answer (pp. 81-82).
- Lognormal walk $S(t)=S(0)e^{(\mu-\sigma^2/2)t+\sigma(X(t)-X(0))}$ (p. 85).
- $e^{-r(T-t)}p_F$ satisfies the PDE with $\mu$; replacing $\mu$ by $r$ gives Black-Scholes, so option value $=e^{-r(T-t)}E[\text{payoff}]$ under the risk-neutral walk (pp. 179-180). Wilmott calls the martingale approach "a bit of a one-trick pony" (p. 180).
- The real-world probability of finishing in the money uses $\mu$ in $d_1'$, so delta is not that probability (p. 181).
- Explicit coefficients $A=\tfrac12(\sigma^2i^2-(r-D)i)\delta t$, $B=-(\sigma^2i^2+r)\delta t$, $C=\tfrac12(\sigma^2i^2+(r-D)i)\delta t$ (p. 1213); stability $c\le0$, $2\nu_1a-\delta t\,c\le1$, $\tfrac12\nu_2|b|\le\nu_1a$, giving $\delta t\le1/(\sigma^2I^2)$ (pp. 1214-1215).
- Crank-Nicolson error $O(\delta t^2,\delta S^2)$ with no relevant time-step limit (p. 1230); projection after the solve is "not good enough" for an implicit scheme, so the payoff constraint goes inside SOR (p. 1246).
- Monte Carlo: exact lognormal stepping (80.1), Euler error $O(\delta t)$, sampling error $O(N^{-1/2})$, choose $N=O(K^{2/3})$, $\delta t=O(K^{-1/3})$ (pp. 1264-1268). No control-variate treatment in the pages read.
- Binary call $e^{-r(T-t)}N(d_2)$; binary call + put $=e^{-r(T-t)}$ (pp. 43-44, 120-121). Barriers: discontinuous delta, "delta hedging through the barrier is virtually impossible" (p. 405); vega meaningless when gamma changes sign (p. 402).
- Geometric Asian: summary on p. 440 says volatility $\sigma/\sqrt3$ and dividend yield $D+\sigma^2/6$; the formula on p. 442 has forward $G\exp[(r-D-\sigma^2/2)(T-t)^2/(2T)+\sigma^2(T-t)^3/(6T^2)]$, which at $t=0$ corresponds to a yield of $\tfrac12(r+D+\sigma^2/6)$. The p. 440 yield is inconsistent with p. 442 (checked numerically: 6.5181 against 5.9802 in the compendium example).
- Hedge with actual volatility: total PV profit $V^a-V^i$ guaranteed, mark-to-market path random and dependent on $\mu$ (pp. 200-202). Hedge with implied: daily profit $\tfrac12(\sigma^2-\tilde\sigma^2)S^2\Gamma^i dt$, eq. (12.1), total "always positive, but highly path dependent" (pp. 202-203); general hedge volatility, eq. (12.2) (p. 203).
- Discrete hedging error $\tfrac12(\phi^2-1)\sigma^2S^2\Gamma\delta t$, chi-squared, mean zero (pp. 769-770).
- Kelly: growth $\approx f\mu-\tfrac12f^2\sigma^2$, eq. (17.1), $f^*=\mu/\sigma^2$, twice Kelly zero expected winnings, half Kelly "halves your volatility ... only decreases your expected growth rate by 25%" (pp. 307-309); continuous growth-optimal weight $(\mu-r)/\sigma^2$ and $J=\log W+(r+(\mu-r)^2/2\sigma^2)(T-t)$ (pp. 1057-1058).

- Lookbacks: updating rule $M_i=\max(S(t_i),M_{i-1})$ and jump condition $V(S,M,t_i^-)=V(S,\max(S,M),t_i^+)$, eq. (24.5) (p. 423); continuous maximum: Black-Scholes for $S<M$ with $\partial V/\partial M=0$ on $S=M$ (p. 447); discrete sampling ``is used to decrease the value'' and the equation then holds for all $S$ (pp. 448-449); payoffs $M^\alpha P(S/M)$ reduce to two dimensions, eq. (26.1) (p. 449); sec. 26.6 formulas agree with Hull sec. 26.11 (checked numerically to $10^{-14}$). No discrete-monitoring correction is printed; Heynen and Kat (1995) are named only (p. 452).
- Transaction costs: Leland's $\check\sigma,\hat\sigma=\sigma(1\mp\sqrt{8/(\pi\delta t)}\,\kappa/\sigma)^{1/2}$ (p. 785); expected cost per step $\sqrt{2/\pi}\kappa\sigma S^2|\Gamma|\delta t^{1/2}$, eq. (48.2); Hoggard-Whalley-Wilmott equation (48.4); (48.5)-(48.6) (pp. 787-788); long-short spread $2\kappa SN'(d_1)\sqrt{T-t}/\sqrt{2\pi\delta t}$ (p. 788); $K=\kappa/(\sigma\delta t^{1/2})$, eq. (48.7). Nonadditivity of portfolio values (pp. 787, 797). Jefferies' tests: 95th-percentile prices 14.90 (Leland, 4 days), 15.15 (delta tolerance), 15.03 (utility); real data 1985-1996, delta tolerance best in nearly 70 percent of cases, utility 23, Leland 7 (pp. 802-806). Costs $\alpha/\sqrt{\delta t}$ against hedging error $\beta\sqrt{\delta t}$ (pp. 807-808).
- Forward (Fokker-Planck) equation $\partial p/\partial t'=\tfrac12\partial^2(B^2p)/\partial y'^2-\partial(Ap)/\partial y'$, eq. (10.2), p. 172; backward equation (10.4), p. 175.

## Limits

- Derivations are heuristic by the author's own description (pp. 78, 82); conditions for Itô and Feynman-Kac are not stated. Neither Girsanov's theorem nor Feynman-Kac is named in the pages read; the risk-neutral link is shown through the backward Kolmogorov equation.
- Market and regulatory statements in the book date from 2006 and are not used.
- Chap. 48, p. 789: the long-position breakdown is printed as $\kappa>\sigma/\sqrt{8\pi\delta t}$, dimensionally inconsistent with (48.5); (48.5) gives $\check\sigma^2>0$ if and only if $\kappa<\sigma\sqrt{\pi\delta t/8}$ ($K<\sqrt{\pi/8}$). The sec. 48.4 heading dates Hoggard-Whalley-Wilmott 1992, the further reading 1994. Chap. 48's empirical results (Jefferies 1999) are dated and not independently checked.

## Implementation

## Notation map

Wilmott writes Brownian motion $X$ (Hull $z$, this compendium $W$), uses calendar time $t$ with expiry $T$ in the PDE, and the asset $S$; the finite-difference chapters use time to expiry (recorded with the later packages).

## Connections

## Entries

`def:brownian-motion-quadratic-variation`, `res:ito-lemma-geometric-brownian-motion`, `res:risk-neutral-pricing-feynman-kac` (`stochastic-processes-calculus`).

Also used for `meth:finite-difference-option-pricing` (`volatility-options`) and the 2026-10-21 extension of `meth:monte-carlo-simulation` (`numerical-optimisation`).

Also used for `meth:digital-option-valuation`, `meth:barrier-option-valuation` and `meth:asian-option-valuation` (`volatility-options`).

Also used for `res:delta-hedging-volatility-mismatch` and the vanna-volga sentence of `meth:greeks-delta-gamma-hedging` (`volatility-options`).

Also used for `res:kelly-growth-optimal-fraction` (`portfolio-construction`).

Also used for `meth:lookback-option-valuation` and `meth:transaction-cost-hedging` (`volatility-options`, Batch L5).

## Open questions
