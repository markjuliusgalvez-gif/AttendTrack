# AttendTrack - Attendance Monitoring System

AttendTrack is a simple command-line **Attendance Monitoring System** written in Python.
It helps a teacher or class officer register students, record daily attendance,
and quickly see who is present, late, or absent, and who is at risk because of low attendance.

## Purpose

Paper attendance sheets are easy to lose and slow to total up. AttendTrack replaces them with a
small program that stores records in CSV files, prevents duplicate entries, and computes
attendance rates automatically. It was created as a group activity on version control with Git and GitHub.

## Features

- Register students (ID, name, course) with duplicate-ID protection
- Take attendance for the whole class on any date, or mark one student
- Three statuses: **Present**, **Late**, **Absent** (re-marking a date corrects the old record)
- View the attendance list of any date
- Per-student summary with attendance rate (Present and Late count as attended)
- **Low-attendance alert** for students below 75%
- Export a class report to CSV (opens in Excel / Google Sheets)
- Remove a student together with their records
- Automated tests

## Requirements

- Python 3.8 or newer (no extra libraries needed)

## How to Run

```bash
git clone https://github.com/markjuliusgalvez-gif/AttendTrack.git
cd AttendTrack
python main.py
```

(On some systems use `python3` instead of `python`.)

### Sample session

```
Choose an option: 1
Student ID: 2024-001
Full name: Ana Cruz
Course (e.g., BSCS): BSCS
Student Ana Cruz (2024-001) added.
```

## Run the Tests

```bash
python -m unittest discover tests
```

## Project Structure

```
AttendTrack/
|-- main.py              # Menu / user interface
|-- students.py          # Student management
|-- attendance.py        # Recording and looking up attendance
|-- reports.py           # Summaries, alerts, CSV export
|-- storage.py           # CSV reading and writing
|-- tests/
|   `-- test_attendtrack.py
|-- docs/
|   `-- DOCUMENTATION.md # Explanation of the main functions
|-- README.md
`-- .gitignore
```

Data is saved automatically in a `data/` folder when the program runs.

## Documentation

See [docs/DOCUMENTATION.md](docs/DOCUMENTATION.md) for an explanation of every main function.

## Contributors

- Mark Julius Galvez (@Rxnzu.git)
- Charles Dave Hafalla (@Chals_Devi)
- Yvette Langas (@yvette)
- Jasmine Vilog (@vilogjasmine06-jpg)

## License

For educational use.
