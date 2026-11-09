"""Branch coverage tests for hospital_triage_priority.py.

BHUVAN KUMAR P (PES1UG24AM069) - Lab 6.

Goal: every decision in the module is taken both ways (True and False),
every loop is run zero times, run to completion and, where possible,
left early. Where a decision combines conditions with `or`, each
condition is tested on its own, and the boundary values (SpO2 90,
heart rate 120, 4 vs 5 flagged entries, 4.0 bar) are checked.
"""

import pytest

from hospital_triage_priority import (monitor_oxygen_manifolds,
                                      process_triage_wards)


def make_ward(patients=None, tier="general", accepting=True,
              icu_standby=False):
    """Build a ward dictionary in the shape the module expects."""
    ward = {"is_accepting": accepting, "tier": tier,
            "icu_standby": icu_standby}
    if patients is not None:
        ward["patients"] = patients
    return ward


NORMAL = {"spo2": 98, "hr": 72, "unconscious": False}
FLAGGED = {"spo2": 0, "hr": 70}


# ---------------------------------------------------------------------
# Line 2: input validation (both conditions of the `or`, and neither)
# ---------------------------------------------------------------------

@pytest.mark.parametrize("wards, default_score", [
    ("not a list", 10),        # isinstance check True
    ({"tier": "general"}, 10),  # a dict is not a list either
    ([], -1),                  # default_acuity_score < 0 True
])
def test_invalid_input_raises(wards, default_score):
    """Decision True: either condition raises ValueError."""
    with pytest.raises(ValueError, match="Invalid wards list"):
        process_triage_wards(wards, default_score)


def test_zero_default_score_is_valid():
    """Decision False at the boundary: a default of 0 is allowed."""
    result = process_triage_wards([make_ward([NORMAL])], 0)
    assert result == {"acuity_score": 0, "status": "NO_URGENT_CASES"}


# ---------------------------------------------------------------------
# Line 8: ward loop (zero iterations, several iterations)
# Line 9: accepting / not accepting / key missing
# ---------------------------------------------------------------------

def test_empty_ward_list():
    """Ward loop runs zero times."""
    assert process_triage_wards([], 10) == {
        "acuity_score": 0, "status": "NO_URGENT_CASES"}


def test_not_accepting_and_missing_flag_are_skipped():
    """Line 9 True: is_accepting False, or missing (defaults to False)."""
    no_flag = {"tier": "general", "patients": [NORMAL]}
    wards = [make_ward([NORMAL], accepting=False), no_flag,
             make_ward([NORMAL])]
    result = process_triage_wards(wards, 10)
    assert result == {"acuity_score": 10, "status": "TRIAGE_STABLE"}


# ---------------------------------------------------------------------
# Line 15: patient loop (zero iterations, completes, exits via break)
# Line 35: icu_standby True / False
# ---------------------------------------------------------------------

def test_ward_without_patients_key_but_icu_standby():
    """Patient loop runs zero times; line 35 True adds 25."""
    result = process_triage_wards([make_ward(icu_standby=True)], 10)
    assert result == {"acuity_score": 25, "status": "TRIAGE_STABLE"}


def test_ward_with_empty_patient_list_and_no_icu():
    """Patient loop runs zero times; line 35 False adds nothing."""
    result = process_triage_wards([make_ward([])], 10)
    assert result == {"acuity_score": 0, "status": "NO_URGENT_CASES"}


# ---------------------------------------------------------------------
# Line 20: invalid vitals (each condition of the `or`, and neither)
# ---------------------------------------------------------------------

@pytest.mark.parametrize("patient", [
    {"spo2": 0, "hr": 80},     # spo2 <= 0
    {"spo2": -5, "hr": 80},    # negative spo2
    {"spo2": 97, "hr": 0},     # hr <= 0
    {"spo2": 97, "hr": -1},    # negative hr
])
def test_invalid_vitals_are_flagged_and_skipped(patient):
    """Decision True: the patient is flagged and adds no acuity."""
    result = process_triage_wards([make_ward([patient, NORMAL])], 10)
    assert result == {"acuity_score": 10, "status": "TRIAGE_STABLE"}


def test_missing_vitals_use_defaults():
    """Decision False: missing spo2/hr default to 95/75 (normal)."""
    result = process_triage_wards([make_ward([{}])], 10)
    assert result == {"acuity_score": 10, "status": "TRIAGE_STABLE"}


# ---------------------------------------------------------------------
# Lines 24 and 26: unconscious patients, outpatient or not
# ---------------------------------------------------------------------

@pytest.mark.parametrize("tier", ["general", "icu", "pediatric"])
def test_unconscious_in_non_outpatient_ward_adds_hundred(tier):
    """Line 24 True, line 26 False: adds 100."""
    patients = [{"spo2": 96, "hr": 80, "unconscious": True}]
    result = process_triage_wards([make_ward(patients, tier=tier)], 10)
    assert result == {"acuity_score": 100, "status": "TRIAGE_STABLE"}


def test_unconscious_in_outpatient_ward_resets_and_breaks():
    """Line 26 True: resets the total to 0 and leaves the patient loop.

    The patient after the unconscious one is never scored.
    """
    patients = [NORMAL, {"unconscious": True}, {"spo2": 80, "hr": 80}]
    result = process_triage_wards([make_ward(patients, tier="outpatient")],
                                  10)
    assert result == {"acuity_score": 0, "status": "NO_URGENT_CASES"}


def test_outpatient_reset_also_clears_earlier_wards():
    """The reset on line 27 discards acuity from previous wards too."""
    wards = [make_ward([{"spo2": 85, "hr": 80}]),             # +60
             make_ward([{"unconscious": True}], tier="outpatient")]
    result = process_triage_wards(wards, 10)
    assert result == {"acuity_score": 0, "status": "NO_URGENT_CASES"}


def test_icu_standby_still_added_after_outpatient_break():
    """After the break, line 35 still runs for the same ward."""
    ward = make_ward([{"unconscious": True}], tier="outpatient",
                     icu_standby=True)
    result = process_triage_wards([ward], 10)
    assert result == {"acuity_score": 25, "status": "TRIAGE_STABLE"}


# ---------------------------------------------------------------------
# Line 30: abnormal vitals (each condition) and boundaries
# ---------------------------------------------------------------------

@pytest.mark.parametrize("spo2, hr, expected", [
    (89, 80, 60),    # spo2 < 90 only
    (97, 121, 60),   # heart_rate > 120 only
    (85, 130, 60),   # both abnormal: still 60, not 120
    (90, 80, 10),    # boundary: spo2 == 90 is not abnormal
    (97, 120, 10),   # boundary: hr == 120 is not abnormal
])
def test_abnormal_vitals_and_boundaries(spo2, hr, expected):
    """Line 30 True adds 60; False falls through to the default."""
    patients = [{"spo2": spo2, "hr": hr, "unconscious": False}]
    result = process_triage_wards([make_ward(patients)], 10)
    assert result == {"acuity_score": expected, "status": "TRIAGE_STABLE"}


# ---------------------------------------------------------------------
# Lines 38 and 40: final status
# ---------------------------------------------------------------------

def test_exactly_four_flagged_is_not_an_alert():
    """Line 38 False at the boundary: 4 flagged entries."""
    patients = [FLAGGED] * 4 + [NORMAL]
    result = process_triage_wards([make_ward(patients)], 10)
    assert result == {"acuity_score": 10, "status": "TRIAGE_STABLE"}


def test_five_flagged_across_wards_is_an_alert():
    """Line 38 True: flagged entries are counted across all wards."""
    wards = [make_ward([FLAGGED] * 3),
             make_ward([FLAGGED, {"unconscious": True}])]  # 3 + 2 = 5
    result = process_triage_wards(wards, 10)
    assert result == {"acuity_score": 100, "status": "WARD_ALERT"}


def test_alert_takes_priority_over_zero_score():
    """Line 38 True wins even when the total acuity is 0."""
    result = process_triage_wards([make_ward([FLAGGED] * 6)], 10)
    assert result == {"acuity_score": 0, "status": "WARD_ALERT"}


def test_mixed_ward_total():
    """Line 40 False: every scoring path adds up correctly."""
    patients = [NORMAL,                                    # +10
                {"spo2": 88, "hr": 80},                    # +60
                {"spo2": 96, "hr": 80, "unconscious": True},  # +100
                FLAGGED]                                   # +0
    result = process_triage_wards([make_ward(patients, icu_standby=True)],
                                  10)                      # +25
    assert result == {"acuity_score": 195, "status": "TRIAGE_STABLE"}


# ---------------------------------------------------------------------
# monitor_oxygen_manifolds
# ---------------------------------------------------------------------

@pytest.mark.parametrize("streams", [[], None])
def test_oxygen_no_data(streams):
    """Line 46 True: empty or None input returns NO_DATA."""
    assert monitor_oxygen_manifolds(streams) == "NO_DATA"


def test_oxygen_empty_manifold_is_normal():
    """Inner loop runs zero times: an empty manifold reads as normal."""
    assert monitor_oxygen_manifolds([[]]) == "PRESSURE_NORMAL"


def test_oxygen_all_readings_normal():
    """Line 52 always False: the loops complete, PRESSURE_NORMAL."""
    assert monitor_oxygen_manifolds([[4.5, 5.0], [6.1]]) == "PRESSURE_NORMAL"


def test_oxygen_exactly_four_bar_is_not_a_drop():
    """Boundary: 4.0 is not below 4.0, so it resets the streak."""
    assert monitor_oxygen_manifolds([[3.9, 4.0, 3.9]]) == "PRESSURE_NORMAL"


def test_oxygen_single_drop_then_recovery():
    """Line 54 False (streak 1), then line 52 False resets it."""
    assert monitor_oxygen_manifolds([[3.5, 5.0, 3.5]]) == "PRESSURE_NORMAL"


def test_oxygen_two_consecutive_drops_fail():
    """Line 54 True: two drops in a row return PRESSURE_FAILURE."""
    assert monitor_oxygen_manifolds([[5.0, 3.9, 3.2, 5.0]]) == \
        "PRESSURE_FAILURE"


def test_oxygen_streak_does_not_carry_between_manifolds():
    """drop_streak resets per manifold: one drop at the end of one
    manifold and one at the start of the next is not a failure."""
    assert monitor_oxygen_manifolds([[5.0, 3.9], [3.9, 5.0]]) == \
        "PRESSURE_NORMAL"


def test_oxygen_failure_in_later_manifold():
    """The outer loop moves on to later manifolds and finds the failure."""
    assert monitor_oxygen_manifolds([[5.0, 5.2], [4.8, 3.1, 2.9]]) == \
        "PRESSURE_FAILURE"
