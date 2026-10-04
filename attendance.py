"""attendance.py - Recording and looking up attendance."""

from datetime import datetime

import storage
import students

STATUSES = {"P": "Present", "L": "Late", "A": "Absent"}


def today_str():
    """Today's date as YYYY-MM-DD."""
    return datetime.now().strftime("%Y-%m-%d")


def is_valid_date(date_str):
    """True if date_str is a real date in YYYY-MM-DD format."""
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def mark_attendance(student_id, date_str, status_code):
    """Record (or correct) one student's attendance for one date.

    status_code is P (Present), L (Late), or A (Absent).
    Returns (success, message).
    """
    status_code = status_code.strip().upper()
    if status_code not in STATUSES:
        return False, "Status must be P (Present), L (Late), or A (Absent)."
    if not is_valid_date(date_str):
        return False, "Date must be a valid date in YYYY-MM-DD format."

    student = students.find_student(student_id)
    if not student:
        return False, "Student not found."

    sid = student["student_id"]
    # Replace any existing record for the same student and date (no duplicates)
    records = [r for r in storage.read_rows(storage.attendance_file())
               if not (r["student_id"] == sid and r["date"] == date_str)]
    records.append({"date": date_str, "student_id": sid,
                    "status": STATUSES[status_code]})
    storage.write_rows(storage.attendance_file(), storage.ATTENDANCE_FIELDS, records)
    return True, f"{student['name']} marked {STATUSES[status_code]} on {date_str}."


def get_attendance_by_date(date_str):
    """Return all attendance records for one date, sorted by student ID."""
    records = [r for r in storage.read_rows(storage.attendance_file())
               if r["date"] == date_str]
    return sorted(records, key=lambda r: r["student_id"])


def get_student_records(student_id):
    """Return all attendance records of one student, sorted by date."""
    sid = student_id.strip().upper()
    records = [r for r in storage.read_rows(storage.attendance_file())
               if r["student_id"].upper() == sid]
    return sorted(records, key=lambda r: r["date"])
