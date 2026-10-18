"""source verification (2026-10-17) (source-review coverage): arithmetic behind figures added from source documents.

1. USGS Mineral Commodity Summaries, February 2026, Aluminum (p. 2): China's share of world smelter production,
   45,000 of 74,000 thousand tonnes in 2025 (estimated) and 44,000 of 72,800 in 2024 (def:metals-markets).
2. EIA, liquefied U.S. natural gas exports, annual, million cubic feet (release of 30 September 2026): 5,508,984 MMcf in
   2025 as billion cubic feet a day, and the growth from 2,924 MMcf in 2013 (def:natural-gas-market).
3. Moallemi and Saglam (revision of 5 February 2013), p. 23, eq. (13): limit-premium reduction in units of the
   standard deviation over the latency interval, sqrt(log(delta^2 / (2 pi sigma^2 dt))), for GS on 4 January 2010
   (delta = $0.058, sigma = $1.92 a day) at 500, 250 and 50 ms, against their 1.4, 1.6 and 2.1; a trading day of
   6.5 hours (23,400 s) is assumed here, which the paper's calibration does not state. Also the latency cost of
   Corollary 1 at 500 ms for the same parameters (not stated in the paper; computed for orientation only).
Run: uv run python commodity-production-latency-checks.py   (standard library). Exits non-zero on failure.
"""

# standard library imports
import math
import sys

fails = []


def check(name, got, want, tol):
    ok = abs(got - want) <= tol
    print(f"  {'ok ' if ok else 'BAD'} {name}: {got:.4f} (want {want}, tol {tol})")
    if not ok:
        fails.append(name)


print("== 1. USGS aluminium")
check("China share of 2025 smelter output", 45_000 / 74_000, 0.61, 0.005)
check("China share of 2024 smelter output", 44_000 / 72_800, 0.60, 0.005)

print("\n== 2. EIA LNG exports")
check("2025 exports, Bcf per day", 5_508_984 / 365 / 1000, 15.1, 0.05)
check("2025 / 2013 ratio (thousands)", 5_508_984 / 2_924 / 1000, 1.884, 0.001)

print("\n== 3. Moallemi-Saglam calibration")
delta, sigma_day, day_s = 0.058, 1.92, 23_400
for ms, want in ((500, 1.4), (250, 1.6), (50, 2.1)):
    sd = sigma_day * math.sqrt(ms / 1000 / day_s)
    check(
        f"adjustment at {ms} ms, in sd units",
        math.sqrt(math.log(delta**2 / (2 * math.pi * sd**2))),
        want,
        0.05,
    )
sd = sigma_day * math.sqrt(0.5 / day_s)
lc = sd / delta * math.sqrt(math.log(delta**2 / (2 * math.pi * sd**2)))
print(
    f"     latency cost (Corollary 1) at 500 ms for these parameters: {lc * 100:.1f}% of the cost of immediacy (orientation only)"
)

if fails:
    print("\nFAILED:", fails)
    sys.exit(1)
print("\nall checks passed")
