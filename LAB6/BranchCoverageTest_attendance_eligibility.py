import pytest
from attendance_eligibility import attendance_percent, exam_eligibility, attendance_warning

# ==============================================================================
# Branch Coverage Test Suite for attendance_eligibility.py
# Designed to cover all decision outcomes (True/False) and boundary conditions.
# ==============================================================================

# ------------------------------------------------------------------------------
# 1. Branch tests for attendance_percent(attended, total_classes, medical_leave_days)
# ------------------------------------------------------------------------------

def test_attendance_percent_zero_or_negative_total_classes():
    # Branch: total_classes <= 0 (True)
    with pytest.raises(ValueError, match="invalid total"):
        attendance_percent(10, 0, 0)
    with pytest.raises(ValueError, match="invalid total"):
        attendance_percent(10, -5, 0)

def test_attendance_percent_negative_attended():
    # Branch: attended < 0 (True)
    with pytest.raises(ValueError, match="invalid attended count"):
        attendance_percent(-1, 50, 0)

def test_attendance_percent_attended_greater_than_total():
    # Branch: attended > total_classes (True)
    with pytest.raises(ValueError, match="invalid attended count"):
        attendance_percent(55, 50, 0)

def test_attendance_percent_medical_leave_greater_than_5():
    # Branch: medical_leave_days > 5 (True) -> capped to 5
    # attended=35, total=50, leave=10 -> credited = 35 + 5 = 40 -> 40*100//50 = 80
    assert attendance_percent(35, 50, 10) == 80

def test_attendance_percent_medical_leave_less_or_equal_5():
    # Branch: medical_leave_days > 5 (False)
    # attended=35, total=50, leave=3 -> credited = 35 + 3 = 38 -> 38*100//50 = 76
    assert attendance_percent(35, 50, 3) == 76
    # Boundary: leave = 5
    assert attendance_percent(35, 50, 5) == 80

def test_attendance_percent_credited_exceeds_total():
    # Branch: credited > total_classes (True) -> capped to total_classes
    # attended=48, total=50, leave=4 -> credited = 52 -> capped to 50 -> 100%
    assert attendance_percent(48, 50, 4) == 100

def test_attendance_percent_credited_within_total():
    # Branch: credited > total_classes (False)
    assert attendance_percent(30, 40, 0) == 75


# ------------------------------------------------------------------------------
# 2. Branch tests for exam_eligibility(percent, has_condonation, fees_paid)
# ------------------------------------------------------------------------------

def test_exam_eligibility_fees_unpaid():
    # Branch: not fees_paid (True)
    assert exam_eligibility(90, True, False) == "fees pending"

def test_exam_eligibility_fees_paid_percent_ge_75():
    # Branch: percent >= 75 (True)
    assert exam_eligibility(75, False, True) == "eligible"
    assert exam_eligibility(85, False, True) == "eligible"

def test_exam_eligibility_percent_65_to_74_with_condonation():
    # Branch: percent >= 65 (True) and has_condonation (True)
    assert exam_eligibility(65, True, True) == "eligible"
    assert exam_eligibility(74, True, True) == "eligible"

def test_exam_eligibility_percent_65_to_74_without_condonation():
    # Branch: percent >= 65 (True) and has_condonation (False)
    assert exam_eligibility(65, False, True) == "condonation required"
    assert exam_eligibility(70, False, True) == "condonation required"

def test_exam_eligibility_percent_below_65():
    # Branch: percent >= 75 (False) and percent >= 65 (False) -> detained
    assert exam_eligibility(64, True, True) == "detained"
    assert exam_eligibility(40, False, True) == "detained"


# ------------------------------------------------------------------------------
# 3. Branch tests for attendance_warning(percent, weeks_left)
# ------------------------------------------------------------------------------

def test_attendance_warning_safe_zone():
    # Branch: percent >= 85 (True)
    assert attendance_warning(85, 10) is None
    assert attendance_warning(95, 2) is None

def test_attendance_warning_critical():
    # Branch: percent < 75 (True) and weeks_left > 4 (True)
    assert attendance_warning(74, 5) == "critical"
    assert attendance_warning(60, 6) == "critical"

def test_attendance_warning_final_notice():
    # Branch: percent < 75 (True) and weeks_left > 4 (False)
    # Boundary: weeks_left == 4
    assert attendance_warning(74, 4) == "final notice"
    assert attendance_warning(50, 1) == "final notice"

def test_attendance_warning_reminder():
    # Branch: percent >= 85 (False) and percent < 75 (False) -> [75, 84]
    assert attendance_warning(75, 5) == "reminder"
    assert attendance_warning(84, 2) == "reminder"
