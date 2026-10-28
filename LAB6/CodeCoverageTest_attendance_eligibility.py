import pytest
from attendance_eligibility import attendance_percent, exam_eligibility, attendance_warning

# --- Tests for attendance_percent ---

def test_attendance_percent_normal():
    assert attendance_percent(30, 40, 0) == 75

def test_attendance_percent_invalid_total():
    with pytest.raises(ValueError, match="invalid total"):
        attendance_percent(10, 0, 0)

def test_attendance_percent_negative_attended():
    with pytest.raises(ValueError, match="invalid attended count"):
        attendance_percent(-1, 10, 0)

def test_attendance_percent_attended_exceeds_total():
    with pytest.raises(ValueError, match="invalid attended count"):
        attendance_percent(15, 10, 0)

def test_attendance_percent_medical_leave_capped():
    # medical_leave_days > 5 gets capped to 5
    assert attendance_percent(20, 30, 8) == 83

def test_attendance_percent_credited_exceeds_total():
    # credited (28 + 4 = 32) > total (30) gets capped to 30
    assert attendance_percent(28, 30, 4) == 100


# --- Tests for exam_eligibility ---

def test_exam_eligibility_fees_unpaid():
    assert exam_eligibility(80, False, False) == "fees pending"

def test_exam_eligibility_eligible_high_percent():
    assert exam_eligibility(80, False, True) == "eligible"

def test_exam_eligibility_with_condonation():
    assert exam_eligibility(70, True, True) == "eligible"

def test_exam_eligibility_without_condonation():
    assert exam_eligibility(70, False, True) == "condonation required"

def test_exam_eligibility_detained():
    assert exam_eligibility(50, True, True) == "detained"


# --- Tests for attendance_warning ---

def test_attendance_warning_safe():
    assert attendance_warning(85, 5) is None

def test_attendance_warning_critical():
    assert attendance_warning(70, 5) == "critical"

def test_attendance_warning_final_notice():
    assert attendance_warning(70, 2) == "final notice"

def test_attendance_warning_reminder():
    assert attendance_warning(80, 2) == "reminder"
