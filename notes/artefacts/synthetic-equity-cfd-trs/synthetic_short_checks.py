"""Numerical checks for res:synthetic-short-put-call (slice 23 follow-up, 2026-10-15).

Run from the repository root:  python3 notes/artefacts/synthetic-equity-cfd-trs/synthetic_short_checks.py
Standard library only. Each check computes the quantity by a route independent of the
closed form it is compared with, and the script exits non-zero if a check fails.
"""
from math import erf, exp, log, pi, sqrt
import sys

TOL = 1e-6
failures = []


def check(name, got, want, tol=TOL):
    ok = abs(got - want) <= tol
    print(f"{'ok  ' if ok else 'FAIL'} {name}: got {got:.6f}, want {want:.6f}")
    if not ok:
        failures.append(name)


# 1. Terminal cash flows, leg by leg, against short stock (-S_T).
K = 95.0
print("1. Terminal cash flows (K = 95): put, -call, bond paying K, total")
for ST in (60.0, 95.0, 100.0, 140.0):
    put = K - ST if ST < K else 0.0          # long put pays only below the strike
    call = ST - K if ST > K else 0.0         # short call owes only above the strike
    package = put - call
    with_long_bond = package + K             # Harris's wording: plus a long bond paying K
    with_short_bond = package - K            # package plus a short bond (borrowing) repaying K
    print(f"   S_T={ST:6.1f}: put {put:6.1f}, call {-call:6.1f}, "
          f"put-call {package:6.1f}, +bond {with_long_bond:6.1f}, -bond {with_short_bond:6.1f}")
    check(f"   put-call = K - S_T at {ST}", package, K - ST)
    check(f"   put-call-bond = -S_T at {ST}", with_short_bond, -ST)
    check(f"   put-call+bond = 2K - S_T at {ST}", with_long_bond, 2 * K - ST)


# 2. European parity by numerical integration over the risk-neutral lognormal density,
#    compared with Black-Scholes closed forms and with K e^{-rT} - S0 e^{-qT}.
def bs(S, K, r, q, s, T):
    N = lambda x: 0.5 * (1 + erf(x / sqrt(2)))
    d1 = (log(S / K) + (r - q + 0.5 * s * s) * T) / (s * sqrt(T))
    d2 = d1 - s * sqrt(T)
    return (S * exp(-q * T) * N(d1) - K * exp(-r * T) * N(d2),
            K * exp(-r * T) * N(-d2) - S * exp(-q * T) * N(-d1))


def by_quadrature(S, K, r, q, s, T, n=200000, zmax=10.0):
    # Integrate over z ~ N(0,1), S_T = S exp((r - q - s^2/2) T + s sqrt(T) z), midpoint rule.
    h = 2 * zmax / n
    c = p = 0.0
    for i in range(n):
        z = -zmax + (i + 0.5) * h
        w = exp(-0.5 * z * z) / sqrt(2 * pi) * h
        ST = S * exp((r - q - 0.5 * s * s) * T + s * sqrt(T) * z)
        c += w * max(ST - K, 0.0)
        p += w * max(K - ST, 0.0)
    return exp(-r * T) * c, exp(-r * T) * p


print("2. European parity, S0=100, K=95, r=5%, q=2%, sigma=25%, T=1")
S0, r, q, s, T = 100.0, 0.05, 0.02, 0.25, 1.0
c_bs, p_bs = bs(S0, K, r, q, s, T)
c_q, p_q = by_quadrature(S0, K, r, q, s, T)
F = S0 * exp((r - q) * T)
print(f"   Black-Scholes C={c_bs:.4f} P={p_bs:.4f} P-C={p_bs - c_bs:.4f}; F={F:.4f}")
check("   call, quadrature vs closed form", c_q, c_bs, 1e-4)
check("   put, quadrature vs closed form", p_q, p_bs, 1e-4)
check("   P-C (quadrature) = K e^-rT - S0 e^-qT", p_q - c_q, K * exp(-r * T) - S0 * exp(-q * T), 1e-4)
check("   P-C = e^-rT (K - F)", p_bs - c_bs, exp(-r * T) * (K - F))


# 3. Rebate comparison with no dividends (q = 0), by day-by-day cash accounts.
#    Short sale: sell one share at S0, the full proceeds held as collateral and credited daily
#    at the rebate r_b (continuously compounded); no fee beyond the rebate shortfall, no extra
#    margin, no recall; buy back at S_T.  Package: buy the put and sell the call at their
#    q = 0 European values, financing or investing P - C at r daily; receive K - S_T at T.
def account(start, rate, T, days=365):
    bal = start
    for _ in range(days):
        bal *= exp(rate * T / days)
    return bal


print("3. Rebate comparison, q = 0, S0=100, K=95, r=5%, sigma=25%, T=1")
c0, p0 = bs(S0, K, r, 0.0, s, T)
premium = p0 - c0
print(f"   q=0 values C={c0:.4f} P={p0:.4f} P-C={premium:.4f} = K e^-rT - S0 = {K * exp(-r * T) - S0:.4f}")
for rb in (0.05, 0.03, -0.01):
    for ST in (80.0, 100.0, 120.0):
        short_sale = account(S0, rb, T) - ST
        package = (K - ST) - account(premium, r, T)
        check(f"   short sale, r_b={rb:+.2f}, S_T={ST}: S0 e^(r_b T) - S_T", short_sale, S0 * exp(rb * T) - ST)
        check(f"   package, S_T={ST}: S0 e^(rT) - S_T", package, S0 * exp(r * T) - ST)
    gap = ((K - 100.0) - account(premium, r, T)) - (account(S0, rb, T) - 100.0)
    check(f"   r_b={rb:+.2f}: package minus short sale = S0 (e^rT - e^(r_b T))", gap,
          S0 * (exp(r * T) - exp(rb * T)))

if failures:
    print(f"{len(failures)} check(s) failed")
    sys.exit(1)
print("all checks passed")
