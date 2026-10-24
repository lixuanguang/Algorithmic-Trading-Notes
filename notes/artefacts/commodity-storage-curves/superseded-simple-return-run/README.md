# Simple-return heating-oil run of 17 October 2026, kept unchanged

`heating_oil_test.py`, its printed results and its monthly panel as committed in `012aa19`, with a copy of the unchanged `backwardation_test.py` it imports. The protocol (`../heating-oil-protocol.md`) defines the held-contract return as a log return, ln(C1(t1)/C2(t)); this run used the simple return C1(t1)/C2(t) − 1 that the imported v2 builder supplies for WTI and gas. An audit in derivatives and empirical validation (2026-10-17) found the mismatch; the corrected script in the parent folder uses the log return for heating oil only (the WTI and gas protocols and outputs are not changed). The premium slope moved from 0.3582 (t 1.67) to 0.3276 (t 1.55) and the out-of-sample R² from −0.92 percent (Clark–West t 0.37) to −0.95 percent (0.31); scarcity is unaffected (it does not use returns). Both runs reject the premium hypothesis. These files reproduce byte for byte when run from a copy of this folder. Do not cite their premium figures as current.

The scripts are no longer kept in the working tree. Each is recoverable byte for byte from the commit that last changed it; to rerun, restore it into a copy of this folder:

```
git show 199ed96a1ddd612a0ba52ca74570aebbaba76a7c:notes/artefacts/commodity-storage-curves/superseded-simple-return-run/backwardation_test.py > backwardation_test.py
git show 199ed96a1ddd612a0ba52ca74570aebbaba76a7c:notes/artefacts/commodity-storage-curves/superseded-simple-return-run/heating_oil_test.py > heating_oil_test.py
```
