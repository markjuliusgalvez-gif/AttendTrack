"""storage.py - Reads and writes the CSV files used by AttendTrack."""

import csv
import os

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

STUDENT_FIELDS = ["student_id", "name", "course"]
ATTENDANCE_FIELDS = ["date", "student_id", "status"]


def set_data_dir(path):
    """Change the folder where data files are stored (used by the tests)."""
    global DATA_DIR
    DATA_DIR = path


def students_file():
    return os.path.join(DATA_DIR, "students.csv")


def attendance_file():
    return os.path.join(DATA_DIR, "attendance.csv")


def ensure_files():
    """Create the data folder and empty CSV files (with headers) if missing."""
    os.makedirs(DATA_DIR, exist_ok=True)
    for path, fields in ((students_file(), STUDENT_FIELDS),
                         (attendance_file(), ATTENDANCE_FIELDS)):
        if not os.path.exists(path):
            write_rows(path, fields, [])


def read_rows(path):
    """Return every row of a CSV file as a list of dictionaries."""
    if not os.path.exists(path):
        return []
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_rows(path, fields, rows):
    """Overwrite a CSV file with the given rows."""
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
