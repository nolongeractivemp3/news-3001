from __future__ import annotations

from pathlib import Path
import sys
from types import SimpleNamespace
import unittest
from unittest.mock import patch

# Allow running this test directly from any working directory.
SERVER_ROOT = Path(__file__).resolve().parents[1]
if str(SERVER_ROOT) not in sys.path:
    sys.path.insert(0, str(SERVER_ROOT))

import myclasses
from db.crud.news import get_news_from_day


def make_news(news_id: str, news_type: str) -> myclasses.News:
    return myclasses.News(
        id=news_id,
        type=news_type,
        title=f"Title {news_id}",
        description="Description",
        full_text="",
        source="Source",
        link=f"https://example.com/{news_id}",
        badges=[],
    )


class FakeDaysCollection:
    def __init__(self, raw_days):
        self.raw_days = raw_days

    def get_full_list(self, query_params=None):
        return self.raw_days


class FakeClient:
    def __init__(self, raw_days):
        self.days = FakeDaysCollection(raw_days)

    def collection(self, name: str):
        if name == "Days":
            return self.days
        raise AssertionError(f"Unexpected collection requested: {name}")


class NewsTypeFilteringTests(unittest.TestCase):
    def setUp(self):
        self.client = FakeClient([SimpleNamespace(news=["n1", "n2", "n3"])])
        self.news_map = {
            "n1": make_news("n1", "google"),
            "n2": make_news("n2", "rss"),
            "n3": make_news("n3", "manual_test"),
        }

    def _get_news_from_id(self, client, news_id: str) -> myclasses.News:
        return self.news_map[news_id]

    def test_without_types_defaults_to_google_and_rss(self):
        with patch("db.crud.news.get_news_from_id", side_effect=self._get_news_from_id):
            result = get_news_from_day(self.client, "2026-02-20")

        self.assertEqual([news.id for news in result], ["n1", "n2"])

    def test_empty_types_returns_no_news(self):
        with patch("db.crud.news.get_news_from_id", side_effect=self._get_news_from_id):
            result = get_news_from_day(self.client, "2026-02-20", [])

        self.assertEqual(result, [])

    def test_google_type_returns_only_google_news(self):
        with patch("db.crud.news.get_news_from_id", side_effect=self._get_news_from_id):
            result = get_news_from_day(self.client, "2026-02-20", ["google"])

        self.assertEqual([news.id for news in result], ["n1"])

    def test_rss_type_returns_only_rss_news(self):
        with patch("db.crud.news.get_news_from_id", side_effect=self._get_news_from_id):
            result = get_news_from_day(self.client, "2026-02-20", ["rss"])

        self.assertEqual([news.id for news in result], ["n2"])

    def test_invalid_type_raises_value_error(self):
        with self.assertRaises(ValueError):
            get_news_from_day(self.client, "2026-02-20", ["newsletter"])


if __name__ == "__main__":
    unittest.main()
