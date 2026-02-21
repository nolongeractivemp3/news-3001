from __future__ import annotations

from pathlib import Path
import sys
import unittest
from unittest.mock import patch

# Allow running this test directly from any working directory.
SERVER_ROOT = Path(__file__).resolve().parents[1]
if str(SERVER_ROOT) not in sys.path:
    sys.path.insert(0, str(SERVER_ROOT))

import myclasses
from scraper.storage import save_day_report


class StorageTestingReportTests(unittest.TestCase):
    def test_testing_mode_uses_preset_report_without_openrouter(self):
        saved_reports: list[myclasses.Report] = []
        saved_days: list[myclasses.Day] = []

        class FakeDatabase:
            def create_report(self, report: myclasses.Report) -> str:
                saved_reports.append(report)
                return "report-test-1"

            def save_day(self, day: myclasses.Day) -> str:
                saved_days.append(day)
                return day.id

        db = FakeDatabase()
        article = myclasses.News(
            id="",
            type="manual_test",
            source="Test Source",
            title="Test Title",
            description="Test Description",
            link="https://example.com/test",
            full_text="",
            badges=[],
        )

        with (
            patch.dict("os.environ", {"SCRAPER_TESTING_MODE": "true"}, clear=False),
            patch("scraper.storage.report.create_and_save_report") as ai_report,
        ):
            save_day_report([article], ["news-1"], db)

        ai_report.assert_not_called()
        self.assertEqual(len(saved_reports), 1)
        self.assertIn("Testbericht", saved_reports[0].text)
        self.assertEqual(len(saved_days), 1)
        self.assertEqual(saved_days[0].reportid, "report-test-1")


if __name__ == "__main__":
    unittest.main()
