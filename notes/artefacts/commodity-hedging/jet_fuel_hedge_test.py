"""meth:time-varying-hedge-ratio, derivatives and empirical validation (2026-10-17): static against rolling minimum-variance hedge ratios
for a Gulf Coast jet-fuel exposure hedged with NYMEX heating-oil or WTI contract 1, out of sample.

Protocol (recorded before any result was computed; committed with the results, not a preregistration):
jet-fuel-hedge-protocol.md. Weekly (last common date of each ISO week) dollar changes per gallon; weeks whose
hedge contract 1 changes delivery month are dropped; static h from the first 260 usable weeks; rolling h from the
previous 104 (sensitivity 52) weeks; out-of-sample variance reduction VR = 1 - Var(dS - h dF)/Var(dS) after week 260.
Run: uv run --frozen --no-editable --group empirical python jet_fuel_hedge_test.py <jet .xls> <folder with EIA_EER_EPD2F_PE1_Y35NY_DPGd.xls> <folder with EIA_RCLC1d.xls>
"""

# standard library imports
import itertools
import os
import sys

# third party library imports
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "commodity-storage-curves"))
# third party library imports
import backwardation_test as bt  # noqa: E402

jet = bt.series(os.path.dirname(sys.argv[1]), os.path.basename(sys.argv[1])[4:-4])
hedges = {
    "HO": (bt.series(sys.argv[2], "EER_EPD2F_PE1_Y35NY_DPGd"), 1.0),
    "WTI": (bt.series(sys.argv[3], "RCLC1d"), 1 / 42),
}
print(f"jet fuel: {min(jet)} to {max(jet)}, {len(jet)} days")


def ols_h(s, f):
    f0 = f - f.mean()
    return float(f0 @ (s - s.mean()) / (f0 @ f0))


for name, (fut, scale) in hedges.items():
    cal = sorted(set(fut))
    common = sorted(set(jet) & set(fut))
    weekly = {}
    for d in common:
        weekly[d.isocalendar()[:2]] = d  # last common date of each ISO week
    wd = [weekly[k] for k in sorted(weekly)]
    dS, dF, used, dropped = [], [], [], 0
    for a, b in itertools.pairwise(wd):
        if bt.delivery(name, cal, a) != bt.delivery(name, cal, b):
            dropped += 1
            continue
        dS.append(jet[b] - jet[a])
        dF.append((fut[b] - fut[a]) * scale)
        used.append(b)
    dS, dF = np.array(dS), np.array(dF)
    print(
        f"\n== hedge: {name} contract 1; {len(dS)} usable weekly changes {used[0]} to {used[-1]}; {dropped} roll weeks dropped"
    )
    h_static = ols_h(dS[:260], dF[:260])
    out = slice(260, None)
    res = {"static (first 260 weeks)": dS[out] - h_static * dF[out]}
    for win in (104, 52):
        hs = np.array([ols_h(dS[i - win : i], dF[i - win : i]) for i in range(260, len(dS))])
        res[f"rolling {win} weeks"] = dS[out] - hs * dF[out]
        if win == 104:
            h_roll = hs
    v0 = dS[out].var(ddof=1)
    print(
        f"  static h = {h_static:.3f}; rolling-104 h ranged {h_roll.min():.3f} to {h_roll.max():.3f}; "
        f"full-sample (in-sample) h = {ols_h(dS, dF):.3f}"
    )
    vr = {k: 1 - v.var(ddof=1) / v0 for k, v in res.items()}
    for k, v in vr.items():
        print(f"  out-of-sample VR, {k}: {v * 100:.1f}%")
    half = (len(dS) - 260) // 2
    for lab, sl in (("first half", slice(0, half)), ("second half", slice(half, None))):
        base = dS[out][sl].var(ddof=1)
        print(
            f"  {lab} ({used[260:][sl][0]} to {used[260:][sl][-1]}): static {1 - res['static (first 260 weeks)'][sl].var(ddof=1) / base:.1%}, "
            f"rolling-104 {1 - res['rolling 104 weeks'][sl].var(ddof=1) / base:.1%}"
        )
    print(
        "  verdict: rolling helps"
        if vr["rolling 104 weeks"] > vr["static (first 260 weeks)"]
        else "  verdict: rolling does not help"
    )
