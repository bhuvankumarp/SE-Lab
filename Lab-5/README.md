# Lab 5: Static Code Analysis (Campus Shuttle Timetable & Fleet Tracker)

**Student:** BHUVAN KUMAR P (PES1UG24AM069)  
**Assigned repo:** [SETAPESU26/L5_07_campus_shuttle](https://github.com/SETAPESU26/L5_07_campus_shuttle)

## Objective

Use Pylint, Bandit and Flake8 to find code-quality, security and style problems in the assigned Python program, and document and fix them, prioritising high and medium severity. Then reflect on the experience.

## Deliverables

| Deliverable | File |
|---|---|
| 1. Cleaned version (at least 4 issues fixed; 14 documented and fixed) | [shuttle_system.py](shuttle_system.py) |
| 2. Issue table | [issues.md](issues.md) |
| 3. Reflection answers | [reflection.md](reflection.md) |
| Tool reports, before | [reports/before/pylint_report.txt](reports/before/pylint_report.txt), [bandit_report.txt](reports/before/bandit_report.txt), [flake8_report.txt](reports/before/flake8_report.txt) |
| Tool reports, after | [reports/after/pylint_report.txt](reports/after/pylint_report.txt), [bandit_report.txt](reports/after/bandit_report.txt), [flake8_report.txt](reports/after/flake8_report.txt) |
| Original assignment instructions | [ASSIGNMENT.md](ASSIGNMENT.md) |

## Results

| Tool | Before | After |
|------|--------|-------|
| Pylint | 6.25/10 | **10.00/10** |
| Bandit | 2 issues (Low) | **0** |
| Flake8 | 10 issues | **0** |

## Commits (one per tool, as required)

1. `Lab 5: add campus shuttle starter and before reports`
2. `Lab 5: fix Bandit issues (B110, B311)`
3. `Lab 5: fix Pylint issues (6.25 -> 10.00/10)`
4. `Lab 5: fix Flake8 issues (PEP 8)`
5. `Lab 5: add after reports, issue table and reflection`

## Run

Requires Python 3.10+. No third-party packages are needed to run it.

```bash
python shuttle_system.py
```

It asks for a route to look up; press Enter for R2. Output with the default:

```
Rejected: invalid passenger count -6 for R2
Rejected: invalid passenger count 'full' for R3
Driver for R1: Prakash
Underused: ['R2']
R1 average: 30.0
R3 average: no valid trips
Route to look up (Enter for R2): Trips on R2 : [4]
```

It writes `fleet.json` in the current folder; this file is git-ignored.

## Re-run the analysis

```bash
pip install pylint bandit flake8
pylint shuttle_system.py > pylint_report.txt
bandit -r shuttle_system.py > bandit_report.txt
flake8 shuttle_system.py > flake8_report.txt
```

Verified with Pylint 4.1.3, Bandit 1.9.4 and Flake8 7.4.1.
