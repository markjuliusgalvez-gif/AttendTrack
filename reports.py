"""reports.py - Attendance summaries, low-attendance alerts, and CSV export."""

import csv
import os

import attendance
import students

LOW_ATTENDANCE_THRESHOLD = 75.0  # percent


def student_summary(student_id):
    """Return a dictionary of attendance counts and rate for one student.

    Present and Late both count as attended.
    Returns None if the student does not exist.
    """
    student = students.find_student(student_id)
    if not student:
        return None

    records = attendance.get_student_records(student["student_id"])
    present = sum(1 for r in records if r["status"] == "Present")
    late = sum(1 for r in records if r["status"] == "Late")
    absent = sum(1 for r in records if r["status"] == "Absent")
    total = present + late + absent
    rate = round((present + late) / total * 100, 1) if total else 0.0

    return {
        "student_id": student["student_id"],
        "name": student["name"],
        "course": student["course"],
        "present": present,
        "late": late,
        "absent": absent,
        "total": total,
        "rate": rate,
    }


def class_summary():
    """Return the summary of every registered student."""
    return [student_summary(s["student_id"]) for s in students.list_students()]


def low_attendance(threshold=LOW_ATTENDANCE_THRESHOLD):
    """Return students who have records and whose rate is below the threshold."""
    return [s for s in class_summary() if s["total"] > 0 and s["rate"] < threshold]


def export_report(filepath=os.path.join("reports", "attendance_report.csv")):
    """Save the class summary to a CSV file. Returns the file path."""
    folder = os.path.dirname(filepath)
    if folder:
        os.makedirs(folder, exist_ok=True)

    fields = ["student_id", "name", "course", "present", "late",
              "absent", "total", "rate"]
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(class_summary())
    return filepath
