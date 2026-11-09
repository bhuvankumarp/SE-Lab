"""Hospital triage input processors, hardened against invalid input.

BHUVAN KUMAR P (PES1UG24AM069) - Lab 7 fixed version.

Every function validates its input and never raises: bad input returns a
message starting with "Invalid" instead of crashing.
"""

import math

# Accepted ranges for each measurement.
HR_RANGE = (1.0, 300.0)        # beats per minute
SPO2_RANGE = (0.0, 100.0)      # percent
TEMP_RANGE = (25.0, 45.0)      # degrees Celsius
WEIGHT_RANGE = (1.0, 500.0)    # kilograms
HEIGHT_RANGE = (0.3, 2.75)     # metres
MAX_BED_NUMBER = 9999

WARD_NAMES = {
    "ER": "Emergency Room",
    "ICU": "Intensive Care Unit",
    "GEN": "General Ward",
    "PED": "Pediatrics",
}


def _to_number(text, label, valid_range):
    """Convert text to a finite float inside valid_range.

    Returns (value, None) on success or (None, error message) on failure.
    """
    try:
        value = float(text.strip())
    except ValueError:
        return None, f"Invalid {label}: {text.strip()!r} is not a number"
    if not math.isfinite(value):
        return None, f"Invalid {label}: {text.strip()!r} is not a finite number"
    low, high = valid_range
    if not low <= value <= high:
        return None, f"Invalid {label}: {value:g} is outside {low:g}-{high:g}"
    return value, None


def parse_vitals_summary(vitals_csv):
    """Summarise 'HR,SpO2,Temp' and classify it as CRITICAL or STABLE."""
    if not isinstance(vitals_csv, str):
        return "Invalid vitals: expected text like '72,98,36.8'"
    parts = vitals_csv.split(',')
    if len(parts) != 3:
        return (f"Invalid vitals: expected 3 comma-separated values "
                f"(HR,SpO2,Temp), got {len(parts)}")
    hr, error = _to_number(parts[0], "heart rate", HR_RANGE)
    if error:
        return error
    spo2, error = _to_number(parts[1], "SpO2", SPO2_RANGE)
    if error:
        return error
    temp, error = _to_number(parts[2], "temperature", TEMP_RANGE)
    if error:
        return error
    critical = hr > 120 or spo2 < 90 or temp > 39.0
    return f"Vitals: HR={hr}, SpO2={spo2}% - {'CRITICAL' if critical else 'STABLE'}"


def compute_patient_bmi(bmi_string):
    """Return BMI (rounded to 2 places) from 'weight/height' in kg/m.

    Returns an "Invalid ..." message instead of a number for bad input.
    """
    if not isinstance(bmi_string, str):
        return "Invalid BMI input: expected text like '70/1.75'"
    parts = bmi_string.split('/')
    if len(parts) != 2:
        return "Invalid BMI input: expected 'weight/height', e.g. '70/1.75'"
    weight, error = _to_number(parts[0], "weight", WEIGHT_RANGE)
    if error:
        return error
    height, error = _to_number(parts[1], "height", HEIGHT_RANGE)
    if error:
        return error
    return round(weight / (height ** 2), 2)


def assign_ward_bed(allocation_code):
    """Describe a 'WARD-bed' code such as 'ICU-05'."""
    if not isinstance(allocation_code, str):
        return "Invalid allocation: expected text like 'ICU-05'"
    parts = allocation_code.strip().split('-')
    if len(parts) != 2:
        return "Invalid allocation: expected 'WARD-bed', e.g. 'ICU-05'"
    ward, bed_str = parts[0].strip().upper(), parts[1].strip()
    if ward not in WARD_NAMES:
        return (f"Invalid allocation: unknown ward {parts[0].strip()!r} "
                f"(use {', '.join(WARD_NAMES)})")
    # isascii() rejects digits like '²' or '٥' that isdigit() accepts.
    if not (bed_str.isascii() and bed_str.isdigit()):
        return f"Invalid allocation: bed {bed_str!r} must be a whole number"
    bed_num = int(bed_str)
    if not 1 <= bed_num <= MAX_BED_NUMBER:
        return f"Invalid allocation: bed number must be 1-{MAX_BED_NUMBER}"
    return f"{WARD_NAMES[ward]} Bed #{bed_num}"


def main():
    """Ask for one input per function and print the results."""
    print("==== Running parse_vitals_summary ====")
    v_input = input("Enter vitals (HR,SpO2,Temp): ")
    print("Summary:", parse_vitals_summary(v_input))

    print("\n==== Running compute_patient_bmi ====")
    b_input = input("Enter weight/height (e.g. 70/1.75): ")
    print("BMI:", compute_patient_bmi(b_input))

    print("\n==== Running assign_ward_bed ====")
    w_input = input("Enter allocation (e.g. ICU-05): ")
    print("Assignment:", assign_ward_bed(w_input))


if __name__ == "__main__":
    main()
