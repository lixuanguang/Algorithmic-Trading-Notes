# First run (v1) of 17 October 2026, kept unchanged

These files are the first run of this pathway's bounded empirical test, as committed in `820517a`. An audit later the same day found implementation problems; the corrected rerun (v2) is the script and outputs in the parent folder, and the reasons for each change are in its docstring and in `notes/source-review-records.md`, *method validation (2026-10-17)*. The v1 outputs still reproduce byte for byte from the retained data with the v1 script (run from a copy, since the script writes its panel next to itself). Do not cite v1 figures as current.

The script is no longer kept in the working tree. Each is recoverable byte for byte from the commit that last changed it; to rerun, restore it into a copy of this folder:

```
git show 199ed96a1ddd612a0ba52ca74570aebbaba76a7c:notes/artefacts/commodity-storage-curves/superseded-first-run/backwardation_test.py > backwardation_test.py
```
