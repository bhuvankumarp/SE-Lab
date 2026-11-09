"""Code (line) coverage tests for hospital_triage_priority.py.

BHUVAN KUMAR P (PES1UG24AM069) - Lab 6.

Goal: execute every line of the module at least once. Each test below
targets the lines named in its docstring. Branch coverage is handled
separately in BranchCoverageTest_PES1UG24AM069_hospital_triage_priority.py.
"""

import pytest

from hospital_triage_priority import (monitor_oxygen_manifolds,
                                      process_triage_wards)


def make_ward(patients, tier="general", accepting=True, icu_standby=False):
    """Build a ward dictionary in the shape the module expects."""
    return {
        "is_accepting": accepting,
        "tier": tier,
        "icu_standby": icu_standby,
        "patients": patients,
    }


NORMAL = {"spo2": 98, "hr": 72, "unconscious": False}


# ---------------------------------------------------------------------
# process_triage_wards
# ---------------------------------------------------------------------

def test_single_normal_patient():
    """Starter test: a normal patient adds the default acuity (line 33)."""
    result = process_triage_wards([make_ward([NORMAL])], 10)
    assert result["acuity_score"] == 10
    assert result["status"] == "TRIAGE_STABLE"


def test_invalid_input_raises_value_error():
    """Line 3: a non-list wards argument is rejected."""
    with pytest.raises(ValueError):
        process_triage_wards("not a list", 10)


def test_ward_not_accepting_is_skipped():
    """Line 10: wards that are not accepting are skipped entirely."""
    wards = [make_ward([NORMAL], accepting=False)]
    result = process_triage_wards(wards, 10)
    assert result == {"acuity_score": 0, "status": "NO_URGENT_CASES"}


def test_invalid_vitals_are_flagged():
    """Lines 21-22: a patient with zero SpO2 is flagged and skipped."""
    patients = [{"spo2": 0, "hr": 80}, NORMAL]
    result = process_triage_wards([make_ward(patients)], 10)
    assert result == {"acuity_score": 10, "status": "TRIAGE_STABLE"}


def test_unconscious_patient_in_general_ward():
    """Lines 25-26, 29: an unconscious patient adds 100."""
    patients = [{"spo2": 96, "hr": 80, "unconscious": True}]
    result = process_triage_wards([make_ward(patients)], 10)
    assert result == {"acuity_score": 100, "status": "TRIAGE_STABLE"}


def test_unconscious_patient_in_outpatient_ward_resets_score():
    """Lines 27-28: outpatient + unconscious resets the score and breaks."""
    patients = [NORMAL, {"unconscious": True}, NORMAL]
    result = process_triage_wards([make_ward(patients, tier="outpatient")], 10)
    assert result == {"acuity_score": 0, "status": "NO_URGENT_CASES"}


def test_abnormal_vitals_add_sixty():
    """Line 31: low SpO2 adds 60."""
    patients = [{"spo2": 85, "hr": 80}]
    result = process_triage_wards([make_ward(patients)], 10)
    assert result == {"acuity_score": 60, "status": "TRIAGE_STABLE"}


def test_icu_standby_adds_twenty_five():
    """Line 36: an ICU standby ward adds 25."""
    result = process_triage_wards([make_ward([NORMAL], icu_standby=True)], 10)
    assert result == {"acuity_score": 35, "status": "TRIAGE_STABLE"}


def test_more_than_four_flagged_entries_raises_ward_alert():
    """Line 39: five flagged entries give WARD_ALERT."""
    patients = [{"spo2": 0, "hr": 70}] * 5
    result = process_triage_wards([make_ward(patients)], 10)
    assert result == {"acuity_score": 0, "status": "WARD_ALERT"}


# ---------------------------------------------------------------------
# monitor_oxygen_manifolds
# ---------------------------------------------------------------------

def test_oxygen_no_data():
    """Line 47: an empty stream list returns NO_DATA."""
    assert monitor_oxygen_manifolds([]) == "NO_DATA"


def test_oxygen_two_consecutive_drops_fail():
    """Lines 52-55: two readings below 4.0 in a row return PRESSURE_FAILURE."""
    assert monitor_oxygen_manifolds([[5.0, 3.5, 3.0]]) == "PRESSURE_FAILURE"


def test_oxygen_isolated_drop_is_normal():
    """Lines 57-58: a single drop resets the streak, giving PRESSURE_NORMAL."""
    assert monitor_oxygen_manifolds([[3.5, 5.0, 3.9, 4.2]]) == "PRESSURE_NORMAL"
