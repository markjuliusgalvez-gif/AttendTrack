"""students.py - Student management (add, find, list, remove)."""

import storage


def list_students():
    """Return all students sorted by student ID."""
    rows = storage.read_rows(storage.students_file())
    return sorted(rows, key=lambda s: s["student_id"])


def find_student(student_id):
    """Return the student with this ID, or None if not found."""
    student_id = student_id.strip().upper()
    for student in storage.read_rows(storage.students_file()):
        if student["student_id"].upper() == student_id:
            return student
    return None


def add_student(student_id, name, course):
    """Register a new student. Returns (success, message)."""
    student_id = student_id.strip().upper()
    name = name.strip()
    course = course.strip()

    if not student_id or not name or not course:
        return False, "Student ID, name, and course are all required."
    if find_student(student_id):
        return False, f"Student ID {student_id} is already registered."

    rows = storage.read_rows(storage.students_file())
    rows.append({"student_id": student_id, "name": name, "course": course})
    storage.write_rows(storage.students_file(), storage.STUDENT_FIELDS, rows)
    return True, f"Student {name} ({student_id}) added."


def remove_student(student_id):
    """Remove a student and all of their attendance records."""
    student = find_student(student_id)
    if not student:
        return False, "Student not found."

    sid = student["student_id"]
    students = [s for s in storage.read_rows(storage.students_file())
                if s["student_id"] != sid]
    storage.write_rows(storage.students_file(), storage.STUDENT_FIELDS, students)

    records = [r for r in storage.read_rows(storage.attendance_file())
               if r["student_id"] != sid]
    storage.write_rows(storage.attendance_file(), storage.ATTENDANCE_FIELDS, records)
    return True, f"Student {student['name']} ({sid}) removed."
