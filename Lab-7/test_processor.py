"""Hypothesis fuzz tests for processor.py.

BHUVAN KUMAR P (PES1UG24AM069) - Lab 7.

Each function must never raise, whatever it is given: bad input must come
back as an "Invalid ..." message instead of an exception. The first three
tests are the starter tests, completed with try/except. The rest build
inputs that are *almost* valid (the right separators with random parts),
which reach deeper into the parsing than random text does, and check that
valid input still gives the right answer.
"""

import math

from hypothesis import given, settings, strategies as st

from processor import assign_ward_bed, compute_patient_bmi, parse_vitals_summary

FUZZ = settings(max_examples=500, deadline=None)

# A number-ish piece of text: real numbers, special floats, or junk.
number_text = st.one_of(
    st.integers(min_value=-10**6, max_value=10**6).map(str),
    st.floats(allow_nan=True, allow_infinity=True).map(str),
    st.sampled_from(["", " ", "nan", "inf", "-inf", "1e400", "0", "-0",
                     "abc", "1,2", "1/2", "١٢", "²"]),
    st.text(max_size=6),
)


def is_invalid_message(result):
    """True when a function reported bad input instead of a result."""
    return isinstance(result, str) and result.startswith("Invalid")


# ---------------------------------------------------------------------
# Starter tests, completed with try/except
# ---------------------------------------------------------------------

@FUZZ
@given(st.text() | st.none())
def test_parse_vitals_summary_no_crash(s):
    """Any text (or None) must not crash parse_vitals_summary."""
    try:
        result = parse_vitals_summary(s)
    except Exception as e:  # pylint: disable=broad-except
        assert False, f"parse_vitals_summary crashed on {s!r} with: {e!r}"
    assert isinstance(result, str)


@FUZZ
@given(st.text() | st.none())
def test_compute_patient_bmi_safe(s):
    """Any text (or None) must not crash compute_patient_bmi."""
    try:
        result = compute_patient_bmi(s)
    except Exception as e:  # pylint: disable=broad-except
        assert False, f"compute_patient_bmi crashed on {s!r} with: {e!r}"
    assert isinstance(result, float) or is_invalid_message(result)


@FUZZ
@given(st.text() | st.none())
def test_assign_ward_bed_safe(s):
    """Any text (or None) must not crash assign_ward_bed."""
    try:
        result = assign_ward_bed(s)
    except Exception as e:  # pylint: disable=broad-except
        assert False, f"assign_ward_bed crashed on {s!r} with: {e!r}"
    assert isinstance(result, str)


# ---------------------------------------------------------------------
# Structured fuzzing: right shape, random parts
# ---------------------------------------------------------------------

@FUZZ
@given(st.lists(number_text, min_size=0, max_size=5))
def test_parse_vitals_structured_no_crash(parts):
    """'a,b,c' style input with random parts and part counts."""
    s = ",".join(parts)
    try:
        result = parse_vitals_summary(s)
    except Exception as e:  # pylint: disable=broad-except
        assert False, f"parse_vitals_summary crashed on {s!r} with: {e!r}"
    assert isinstance(result, str)


@FUZZ
@given(st.lists(number_text, min_size=0, max_size=4))
def test_compute_patient_bmi_structured_no_crash(parts):
    """'w/h' style input: zero, negative, huge, nan and inf values."""
    s = "/".join(parts)
    try:
        result = compute_patient_bmi(s)
    except Exception as e:  # pylint: disable=broad-except
        assert False, f"compute_patient_bmi crashed on {s!r} with: {e!r}"
    assert isinstance(result, float) or is_invalid_message(result)
    if isinstance(result, float):
        assert math.isfinite(result) and result > 0


@FUZZ
@given(st.sampled_from(["ER", "icu", "Gen", "PED", "XYZ", "", " ICU"]),
       st.lists(number_text, min_size=0, max_size=3))
def test_assign_ward_bed_structured_no_crash(ward, beds):
    """'WARD-bed' style input: unknown wards, odd bed text, extra dashes."""
    s = "-".join([ward] + beds)
    try:
        result = assign_ward_bed(s)
    except Exception as e:  # pylint: disable=broad-except
        assert False, f"assign_ward_bed crashed on {s!r} with: {e!r}"
    assert isinstance(result, str)


# ---------------------------------------------------------------------
# Properties: valid input still gives the right answer
# ---------------------------------------------------------------------

@FUZZ
@given(st.integers(1, 300), st.integers(0, 100),
       st.floats(25.0, 45.0).map(lambda t: round(t, 1)))
def test_parse_vitals_valid_input(hr, spo2, temp):
    """Valid vitals are summarised and classified correctly."""
    result = parse_vitals_summary(f"{hr},{spo2},{temp}")
    critical = hr > 120 or spo2 < 90 or temp > 39.0
    assert result == (f"Vitals: HR={float(hr)}, SpO2={float(spo2)}% - "
                      f"{'CRITICAL' if critical else 'STABLE'}")


@FUZZ
@given(st.floats(1.0, 500.0), st.floats(0.3, 2.7))
def test_compute_patient_bmi_valid_input(weight, height):
    """Valid weight/height gives weight / height^2, rounded to 2 places."""
    assert compute_patient_bmi(f"{weight}/{height}") == round(
        weight / height ** 2, 2)


@FUZZ
@given(st.sampled_from(["ER", "ICU", "GEN", "PED"]), st.integers(1, 9999),
       st.booleans())
def test_assign_ward_bed_valid_input(ward, bed, lower):
    """Known wards (any case) and positive bed numbers are accepted."""
    code = f"{ward.lower() if lower else ward}-{bed:02d}"
    result = assign_ward_bed(code)
    names = {"ER": "Emergency Room", "ICU": "Intensive Care Unit",
             "GEN": "General Ward", "PED": "Pediatrics"}
    assert result == f"{names[ward]} Bed #{bed}"
