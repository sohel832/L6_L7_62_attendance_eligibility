# LAB 6 — Attendance Eligibility Coverage Analysis

## About

This directory contains the source application and test suites for **Lab 6: Code and Branch Coverage Analysis**.

## Files Overview

| File | Description |
|------|-------------|
| `attendance_eligibility.py` | The core Python module under test |
| `test_attendance_eligibility.py` | Complete synchronized test suite |
| `CodeCoverageTest_attendance_eligibility.py` | Test suite achieving **100% Code Coverage** |
| `BranchCoverageTest_attendance_eligibility.py` | Test suite achieving **100% Branch Coverage** (22/22 branches) |
| `code_coverage.png` | Terminal output screenshot for code coverage |
| `branch_coverage.png` | Terminal output screenshot for branch coverage |

---

## Commands to Verify

### 1. Code Coverage
```powershell
coverage run -m pytest CodeCoverageTest_attendance_eligibility.py
coverage report -m
```

### 2. Branch Coverage
```powershell
coverage run --branch -m pytest BranchCoverageTest_attendance_eligibility.py
coverage report -m
```

---

## Results Summary

* **Line Coverage:** **100%** (0 lines missed)
* **Branch Coverage:** **100%** (22 out of 22 branches covered)
