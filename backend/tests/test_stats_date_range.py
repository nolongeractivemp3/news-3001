import datetime
import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch

HELPERS_PATH = (
    Path(__file__).resolve().parents[1] / "db" / "crud" / "stats" / "_helpers.py"
)
SPEC = importlib.util.spec_from_file_location("stats_helpers", HELPERS_PATH)
stats_helpers = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(stats_helpers)

DEFAULT_DAYS_WINDOW = stats_helpers.DEFAULT_DAYS_WINDOW
resolve_date_range = stats_helpers.resolve_date_range


class ResolveDateRangeTests(unittest.TestCase):
    def test_defaults_to_last_30_days_when_no_dates_provided(self):
        fake_today = datetime.date(2026, 3, 26)

        with patch.object(stats_helpers.datetime, "date") as mock_date:
            mock_date.today.return_value = fake_today
            mock_date.side_effect = lambda *args, **kwargs: datetime.date(*args, **kwargs)

            start_date, end_date = resolve_date_range()

        self.assertEqual(end_date, fake_today)
        self.assertEqual(
            start_date, fake_today - datetime.timedelta(days=DEFAULT_DAYS_WINDOW - 1)
        )

    def test_rejects_partial_ranges(self):
        with self.assertRaisesRegex(
            ValueError, "Both start_date and end_date are required together."
        ):
            resolve_date_range(start_date_string="2026-03-01")

    def test_rejects_reversed_ranges(self):
        with self.assertRaisesRegex(
            ValueError, "start_date must be on or before end_date."
        ):
            resolve_date_range("2026-03-10", "2026-03-01")

    def test_rejects_ranges_longer_than_max_window(self):
        with self.assertRaisesRegex(
            ValueError, "Date range must be between 1 and 365 days inclusive."
        ):
            resolve_date_range("2025-01-01", "2026-01-02")

    def test_accepts_valid_custom_range(self):
        start_date, end_date = resolve_date_range("2026-03-01", "2026-03-26")

        self.assertEqual(start_date, datetime.date(2026, 3, 1))
        self.assertEqual(end_date, datetime.date(2026, 3, 26))


if __name__ == "__main__":
    unittest.main()
