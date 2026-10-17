"""def:crypto-venue-structure, empirical extensions (2026-10-17): one-day snapshot of Deribit's listed options.

Reads Deribit's public API responses saved on 2026-10-17 (reading_materials/empirical-extensions/deribit):
  public/get_instruments?currency={BTC,ETH,USDC}&kind=option&expired=false  -> listing, settlement, instrument type;
  public/get_book_summary_by_currency?currency={BTC,USDC}&kind=option       -> open interest per instrument.
Reports, for BTC options: inverse (coin-settled, 'reversed') against USDC-settled linear listings, expiries, strikes
per expiry, and how concentrated open interest is across expiries and strikes. A snapshot of one venue on one day;
no other venue was read, so it says nothing about "fewer venues" and is not a time series.
Run: python3 deribit-options-snapshot.py <reading_materials/empirical-extensions/deribit>
"""
import collections
import json
import os
import sys

D = sys.argv[1]


def load(name):
    with open(os.path.join(D, name)) as f:
        return json.load(f)['result']


for cur in ('BTC', 'ETH', 'USDC'):
    ins = load(f'instruments_{cur}_option.json')
    kinds = collections.Counter((x['base_currency'], x['settlement_currency'], x['instrument_type']) for x in ins)
    for (base, settle, typ), n in sorted(kinds.items()):
        exp = collections.Counter(x['expiration_timestamp'] for x in ins
                                  if (x['base_currency'], x['settlement_currency'], x['instrument_type']) == (base, settle, typ))
        strikes = sorted(v // 2 for v in exp.values())
        print(f'{cur:4s} file: {base:5s} settled in {settle:4s} ({typ:8s}) {n:4d} instruments, {len(exp):2d} expiries, '
              f'strikes per expiry median {strikes[len(strikes) // 2]}, max {strikes[-1]}')

for cur, base in (('BTC', 'BTC'), ('USDC', 'BTC')):
    bs = [x for x in load(f'book_summary_{cur}_option.json') if x['instrument_name'].split('-')[0] in (base, base + '_USDC')]
    oi = [x['open_interest'] for x in bs]
    tot = sum(oi)
    srt = sorted(oi, reverse=True)
    top = lambda k: sum(srt[:k]) / tot * 100
    by_exp = collections.Counter()
    by_strike = collections.Counter()
    for x in bs:
        _, e, k, _cp = x['instrument_name'].split('-')
        by_exp[e] += x['open_interest']
        by_strike[k] += x['open_interest']
    spot = bs[0]['estimated_delivery_price']
    print(f'\n{base} options settled in {"BTC (inverse)" if cur == "BTC" else "USDC (linear)"}: {len(bs)} instruments, '
          f'open interest {tot:,.1f} BTC, index {spot:,.0f}; zero-OI instruments {sum(v == 0 for v in oi)}')
    print(f'  share of open interest in top 1% / 5% / 10% of instruments: '
          f'{top(max(1, len(oi) // 100)):.1f}% / {top(len(oi) // 20):.1f}% / {top(len(oi) // 10):.1f}%')
    e1 = by_exp.most_common(3)
    print('  largest expiries: ' + ', '.join(f'{e} {v / tot * 100:.1f}%' for e, v in e1))
    s1 = by_strike.most_common(5)
    print('  largest strikes (all expiries): ' + ', '.join(f'{k} {v / tot * 100:.1f}%' for k, v in s1))
    if cur == 'BTC':
        inv_oi = tot
    else:
        print(f'  USDC-settled BTC open interest relative to inverse: {tot / inv_oi * 100:.1f}%')
