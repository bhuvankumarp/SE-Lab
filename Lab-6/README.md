# Lab 6: Code and Branch Coverage Analysis (Hospital Triage Priority)

**Student:** BHUVAN KUMAR P (PES1UG24AM069)  
**Assigned repo:** [SETAPESU26/L6_L7_07_hospital_traige_priority](https://github.com/SETAPESU26/L6_L7_07_hospital_traige_priority)

## Objective

Measure line and branch coverage of `hospital_triage_priority.py` with `coverage` and `pytest`, then write test cases that reach at least 90% code coverage and at least 90% branch coverage.

## Deliverables

| Deliverable | File |
|---|---|
| Test cases for code coverage | [CodeCoverageTest_PES1UG24AM069_hospital_triage_priority.py](CodeCoverageTest_PES1UG24AM069_hospital_triage_priority.py) |
| Test cases for branch coverage | [BranchCoverageTest_PES1UG24AM069_hospital_triage_priority.py](BranchCoverageTest_PES1UG24AM069_hospital_triage_priority.py) |
| Code coverage screenshots | [01_code_coverage_line_report.png](screenshots/01_code_coverage_line_report.png), [02_code_coverage_branch_report.png](screenshots/02_code_coverage_branch_report.png) |
| Branch coverage screenshots | [03_branch_coverage_branch_report.png](screenshots/03_branch_coverage_branch_report.png), [04_branch_coverage_line_report.png](screenshots/04_branch_coverage_line_report.png) |
| Module under test (unchanged) | [hospital_triage_priority.py](hospital_triage_priority.py) |
| Starter test (unchanged) | [test_hospital_triage.py](test_hospital_triage.py) |
| Original assignment README | [ASSIGNMENT.md](ASSIGNMENT.md) |

The screenshots are images of the real terminal output of the commands below, run in this folder.

## Results for `hospital_triage_priority.py`

| Test file | Tests | Line coverage | Branch coverage |
|---|---|---|---|
| `test_hospital_triage.py` (starter) | 1 | 47% (24 of 45 lines missed) | 43% (8 partial branches) |
| `CodeCoverageTest_…` | 12 | **100%** | 100% |
| `BranchCoverageTest_…` | 37 | **100%** | **100%** (32/32 branches, 0 partial) |

## Approach

- **Code coverage file (12 tests):** one test per uncovered line in the starter report:
  - the `ValueError`;
  - a skipped non-accepting ward;
  - invalid vitals;
  - an unconscious patient in a general ward and in an outpatient ward;
  - abnormal vitals;
  - ICU standby;
  - `WARD_ALERT`;
  - each oxygen outcome (`NO_DATA`, `PRESSURE_FAILURE`, `PRESSURE_NORMAL`).

  Because the module is small, these tests also happen to take every branch, so branch coverage reaches 100% too.
- **Branch coverage file (37 tests):** tests each decision on purpose, both ways:
  - each side of the `or` conditions on lines 2, 20 and 30 on its own;
  - loops that run zero times (no wards, no patients, an empty manifold), run to completion, or exit early (the outpatient `break`, an early `PRESSURE_FAILURE` return);
  - the boundary values: SpO2 = 90 and heart rate = 120 are *not* abnormal, 4 flagged entries is *not* an alert but 5 is, and 4.0 bar is *not* a pressure drop.

## Behaviour the tests document

These are how the module behaves today; the tests assert it and the module was not changed:
- An unconscious patient in an **outpatient** ward sets the total to 0 for **all** wards scored so far, not just that ward. The patients after them in that ward are skipped.
- `icu_standby` still adds 25 for a ward after that `break`.
- A patient with both low SpO2 and a high heart rate adds 60, not 120.
- `drop_streak` resets for each manifold, so a drop at the end of one manifold and another at the start of the next is not a failure.

## Run

```bash
pip install coverage pytest

# Code coverage
coverage run -m pytest CodeCoverageTest_PES1UG24AM069_hospital_triage_priority.py
coverage report -m

# Branch coverage
coverage run --branch -m pytest BranchCoverageTest_PES1UG24AM069_hospital_triage_priority.py
coverage report -m
```

Pass the test file name as shown. Plain `pytest` only auto-discovers files named `test_*.py`, so on its own it runs just the starter test.

Verified with Python 3.11, pytest 9.2.0 and Coverage.py 7.17.2.

## Commits

1. `Lab 6: add hospital triage starter code`
2. `Lab 6: add code coverage test cases and report screenshots`
3. `Lab 6: add branch coverage test cases and report screenshots`
4. `Lab 6: add README`
