# Lab 7: Fuzzing for Input Validation Bugs (Hospital Triage Processor)

**Student:** BHUVAN KUMAR P (PES1UG24AM069)  
**Assigned repo:** [SETAPESU26/L6_L7_07_hospital_traige_priority](https://github.com/SETAPESU26/L6_L7_07_hospital_traige_priority) (Lab 7)

## Objective

Use the Hypothesis property-based fuzzing library to find input validation bugs in `processor.py`, then harden the program against them.

## Deliverables

| Deliverable | File |
|---|---|
| 1. PDF document with the screenshots | [Lab7_FuzzTesting_PES1UG24AM069.pdf](Lab7_FuzzTesting_PES1UG24AM069.pdf) |
| 2. Fixed application script | [processor.py](processor.py) |
| 3. Updated test file | [test_processor.py](test_processor.py) |
| Screenshots (also inside the PDF) | [step2](screenshots/step2_buggy_processor_output.png), [step4](screenshots/step4_fuzz_tests_failing.png), [step5](screenshots/step5_fixed_processor_output.png), [step6](screenshots/step6_fuzz_tests_passing.png) |
| Full failing pytest output (buggy code) | [fuzz_results_buggy.txt](fuzz_results_buggy.txt) |
| Original assignment README | [ASSIGNMENT.md](ASSIGNMENT.md) |

The original buggy `processor.py` and the starter `test_processor.py` are in this folder's first commit (`Lab 7: add hospital triage processor starter code`).

## Results

| Run | Result |
|---|---|
| `python -m pytest test_processor.py` on the buggy code | **6 failed**, 3 passed |
| `python -m pytest test_processor.py` on the fixed code | **9 passed** (also 9 passed at 5,000 examples per test) |

## Tests in `test_processor.py`

- **Starter tests, completed with try/except** (`@given(st.text() | st.none())`): any exception fails the test.
  - `test_parse_vitals_summary_no_crash`
  - `test_compute_patient_bmi_safe`
  - `test_assign_ward_bed_safe`
- **Structured fuzzers:** build almost-valid input (`a,b,c`, `w/h`, `WARD-bed`) from random numbers, `nan`/`inf`, empty and junk text, so the fuzzing gets past the first `split`.
- **Property tests:** valid vitals, BMI and ward codes still give exactly the right result.

## Bugs found and fixed

| Function | Example input | Failure (buggy code) | Fix |
|---|---|---|---|
| All three | `None` | `AttributeError` on `.split()` / `.strip()` | Reject anything that is not a string |
| `parse_vitals_summary` | `'0'`, `'0,0'` | `IndexError` | Require exactly 3 values |
| `parse_vitals_summary` | `''`, `'0,0,'` | `ValueError` (float conversion) | Parse each value safely |
| `parse_vitals_summary` | `'nan,nan,nan'` | No crash, but reported as `STABLE` | Reject non-finite and out-of-range values |
| `compute_patient_bmi` | `''`, `'70'` | `ValueError` (unpack) | Require exactly one `/` |
| `compute_patient_bmi` | `'/'`, `'0/'`, `'/0'` | `ValueError` (float conversion) | Parse weight and height safely |
| `compute_patient_bmi` | `'0/0'`, `'70/0'` | `ZeroDivisionError` | Weight 1–500 kg, height 0.3–2.75 m |
| `assign_ward_bed` | `''`, `'ER'` | `ValueError` (unpack) | Require exactly one `-` |
| `assign_ward_bed` | `'-'`, `'ER-0.0'` | `ValueError` (`int()`) | Bed must be ASCII digits, 1–9999 |
| `assign_ward_bed` | `'XYZ-05'` | `KeyError` | Check the ward against the known list |

Bad input now returns a message starting with `Invalid` instead of raising. Valid input gives the same output as the original.

## Run

```bash
pip install hypothesis pytest
python processor.py
python -m pytest test_processor.py
```

Verified with Python 3.11, pytest 9.2.0 and Hypothesis 6.170.15.
