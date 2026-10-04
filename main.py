"""main.py - Command-line menu for AttendTrack (Attendance Monitoring System)."""

import attendance
import reports
import storage
import students

MENU = """
========== AttendTrack ==========
 1. Add student
 2. View all students
 3. Take attendance (whole class)
 4. Mark attendance (one student)
 5. View attendance by date
 6. View student attendance summary
 7. Low-attendance alert
 8. Export class report (CSV)
 9. Remove student
 0. Exit
=================================
"""


def ask_date():
    """Ask for a date; pressing Enter uses today's date."""
    value = input(f"Date (YYYY-MM-DD) [Enter = {attendance.today_str()}]: ").strip()
    return value or attendance.today_str()


def add_student_menu():
    sid = input("Student ID: ")
    name = input("Full name: ")
    course = input("Course (e.g., BSCS): ")
    print(students.add_student(sid, name, course)[1])


def view_students_menu():
    rows = students.list_students()
    if not rows:
        print("No students registered yet.")
        return
    print(f"\n{'ID':<12}{'Name':<28}{'Course'}")
    print("-" * 52)
    for s in rows:
        print(f"{s['student_id']:<12}{s['name']:<28}{s['course']}")


def take_attendance_menu():
    rows = students.list_students()
    if not rows:
        print("No students registered yet.")
        return
    date_str = ask_date()
    if not attendance.is_valid_date(date_str):
        print("Invalid date. Use YYYY-MM-DD.")
        return
    print("Enter P = Present, L = Late, A = Absent (Enter = skip)")
    for s in rows:
        code = input(f"{s['student_id']} - {s['name']}: ").strip()
        if code:
            print("  ", attendance.mark_attendance(s["student_id"], date_str, code)[1])


def mark_one_menu():
    sid = input("Student ID: ")
    date_str = ask_date()
    code = input("Status (P/L/A): ")
    print(attendance.mark_attendance(sid, date_str, code)[1])


def view_by_date_menu():
    date_str = ask_date()
    if not attendance.is_valid_date(date_str):
        print("Invalid date. Use YYYY-MM-DD.")
        return
    records = attendance.get_attendance_by_date(date_str)
    if not records:
        print(f"No attendance recorded for {date_str}.")
        return
    names = {s["student_id"]: s["name"] for s in students.list_students()}
    print(f"\nAttendance for {date_str}")
    print(f"{'ID':<12}{'Name':<28}{'Status'}")
    print("-" * 52)
    for r in records:
        print(f"{r['student_id']:<12}{names.get(r['student_id'], '?'):<28}{r['status']}")


def student_summary_menu():
    s = reports.student_summary(input("Student ID: "))
    if not s:
        print("Student not found.")
        return
    print(f"\n{s['name']} ({s['student_id']}) - {s['course']}")
    print(f"Present: {s['present']}  Late: {s['late']}  Absent: {s['absent']}")
    print(f"Total days: {s['total']}  Attendance rate: {s['rate']}%")


def low_attendance_menu():
    rows = reports.low_attendance()
    if not rows:
        print(f"No students below {reports.LOW_ATTENDANCE_THRESHOLD}% attendance.")
        return
    print(f"\nStudents below {reports.LOW_ATTENDANCE_THRESHOLD}% attendance:")
    for s in rows:
        print(f" - {s['name']} ({s['student_id']}): {s['rate']}% "
              f"({s['absent']} absent of {s['total']} days)")


def export_menu():
    path = reports.export_report()
    print(f"Report saved to {path}")


def remove_student_menu():
    sid = input("Student ID to remove: ")
    confirm = input("This also deletes their attendance records. Type YES to confirm: ")
    if confirm.strip() == "YES":
        print(students.remove_student(sid)[1])
    else:
        print("Cancelled.")


ACTIONS = {
    "1": add_student_menu,
    "2": view_students_menu,
    "3": take_attendance_menu,
    "4": mark_one_menu,
    "5": view_by_date_menu,
    "6": student_summary_menu,
    "7": low_attendance_menu,
    "8": export_menu,
    "9": remove_student_menu,
}


def main():
    storage.ensure_files()
    while True:
        print(MENU)
        choice = input("Choose an option: ").strip()
        if choice == "0":
            print("Goodbye!")
            break
        action = ACTIONS.get(choice)
        if action:
            action()
        else:
            print("Invalid choice. Please enter a number from the menu.")


if __name__ == "__main__":
    main()
