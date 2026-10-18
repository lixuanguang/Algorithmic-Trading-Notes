"""derivatives and empirical validation (2026-10-17): one-day snapshot of OKX's BTC option listings and open interest, for comparison
with empirical extensions (2026-10-17)'s Deribit snapshot (def:crypto-venue-instrument-structure). Descriptive only.

Inputs (OKX public REST API v5, retrieved 2026-10-17 about 11:52 UTC): /api/v5/public/instruments?instType=OPTION&uly=BTC-USD
and /api/v5/public/open-interest?instType=OPTION&uly=BTC-USD. Reported: instrument counts by settlement currency and
contract type, expiries, open interest (oiUsd) by contract type, by expiry and in the ten largest instruments.
Run: uv run python okx-options-snapshot.py <instruments.json> <open-interest.json>
"""

# standard library imports
import collections
import datetime as dt
import json
import sys

ins = json.load(open(sys.argv[1]))["data"]
oi = json.load(open(sys.argv[2]))["data"]
typ = {i["instId"]: (i["settleCcy"], i["ctType"]) for i in ins}
print(
    f"snapshot time {dt.datetime.utcfromtimestamp(int(oi[0]['ts']) / 1000):%Y-%m-%d %H:%M} UTC; {len(ins)} BTC option instruments"
)
for k, v in sorted(
    collections.Counter(
        (i["settleCcy"], i["ctType"], i["ctMult"], i["ctValCcy"]) for i in ins
    ).items()
):
    print(f"  settle {k[0]}, {k[1]}, multiplier {k[2]} {k[3]}: {v} instruments")
for t in ("inverse", "linear"):
    print(f"  {t} expiries: {len({i['expTime'] for i in ins if i['ctType'] == t})}")
ou = {x["instId"]: float(x["oiUsd"]) for x in oi}
tot = sum(ou.values())
agg = collections.Counter()
for k, v in ou.items():
    agg[typ.get(k, ("?", "?"))[1]] += v
print(
    f"open interest USD {tot / 1e9:.3f} bn: "
    + ", ".join(f"{k} {v / tot:.1%}" for k, v in agg.most_common())
)
byexp = collections.Counter()
for k, v in ou.items():
    byexp[k.replace("_UM", "").split("-")[2]] += v
top3 = byexp.most_common(3)
print(
    "largest expiries: "
    + ", ".join(f"{e} {v / tot:.1%}" for e, v in top3)
    + f" (together {sum(v for _, v in top3) / tot:.1%})"
)
top10 = sorted(ou.items(), key=lambda x: -x[1])[:10]
print(
    f"ten largest instruments hold {sum(v for _, v in top10) / tot:.1%}; largest: "
    + ", ".join(f"{k} {v / tot:.1%}" for k, v in top10[:3])
)
