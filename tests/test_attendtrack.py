"""Automated tests for AttendTrack. Run from the project root:
    python -m unittest discover tests
"""

import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import attendance
import reports
import storage
import students


class AttendTrackTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        storage.set_data_dir(self.tmp.name)
        storage.ensure_files()
        students.add_student("2024-001", "Ana Cruz", "BSCS")
        students.add_student("2024-002", "Ben Reyes", "BSCS")

    def tearDown(self):
        self.tmp.cleanup()

    def test_add_student_and_reject_duplicate(self):
        self.assertEqual(len(students.list_students()), 2)
        ok, _ = students.add_student("2024-001", "Someone Else", "BSIT")
        self.assertFalse(ok)

    def test_add_student_requires_all_fields(self):
        ok, _ = students.add_student("", "No Id", "BSCS")
        self.assertFalse(ok)

    def test_mark_attendance_and_correction(self):
        ok, _ = attendance.mark_attendance("2024-001", "2026-10-01", "A")
        self.assertTrue(ok)
        attendance.mark_attendance("2024-001", "2026-10-01", "P")  # correction
        records = attendance.get_attendance_by_date("2026-10-01")
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["status"], "Present")

    def test_invalid_inputs(self):
        self.assertFalse(attendance.mark_attendance("2024-001", "2026-13-40", "P")[0])
        self.assertFalse(attendance.mark_attendance("2024-001", "2026-10-01", "X")[0])
        self.assertFalse(attendance.mark_attendance("9999", "2026-10-01", "P")[0])

    def test_summary_rate(self):
        attendance.mark_attendance("2024-001", "2026-10-01", "P")
        attendance.mark_attendance("2024-001", "2026-10-02", "L")
        attendance.mark_attendance("2024-001", "2026-10-03", "A")
        attendance.mark_attendance("2024-001", "2026-10-04", "A")
        s = reports.student_summary("2024-001")
        self.assertEqual((s["present"], s["late"], s["absent"], s["total"]), (1, 1, 2, 4))
        self.assertEqual(s["rate"], 50.0)

    def test_low_attendance_alert(self):
        for day in ("2026-10-01", "2026-10-02"):
            attendance.mark_attendance("2024-001", day, "P")
            attendance.mark_attendance("2024-002", day, "A")
        low = reports.low_attendance()
        self.assertEqual([s["student_id"] for s in low], ["2024-002"])

    def test_remove_student_deletes_records(self):
        attendance.mark_attendance("2024-002", "2026-10-01", "P")
        students.remove_student("2024-002")
        self.assertIsNone(students.find_student("2024-002"))
        self.assertEqual(attendance.get_student_records("2024-002"), [])

    def test_export_report(self):
        attendance.mark_attendance("2024-001", "2026-10-01", "P")
        path = os.path.join(self.tmp.name, "out", "report.csv")
        reports.export_report(path)
        self.assertTrue(os.path.exists(path))


if __name__ == "__main__":
    unittest.main()
