from __future__ import annotations

from pathlib import Path
import sys
import unittest

# Allow running this test directly from any working directory.
SERVER_ROOT = Path(__file__).resolve().parents[1]
if str(SERVER_ROOT) not in sys.path:
    sys.path.insert(0, str(SERVER_ROOT))

from db.crud.news import get_unique_news_sources


class _RawNews:
    def __init__(self, source):
        self.source = source


class _FakeNewsCollection:
    def __init__(self, rows):
        self.rows = rows
        self.query_params = None

    def get_full_list(self, query_params=None):
        self.query_params = query_params
        return self.rows


class _FakeClient:
    def __init__(self, rows):
        self.news_collection = _FakeNewsCollection(rows)

    def collection(self, name: str):
        if name != "news":
            raise ValueError(f"Unexpected collection: {name}")
        return self.news_collection


class UniqueNewsSourcesTests(unittest.TestCase):
    def test_returns_sorted_unique_trimmed_sources(self):
        rows = [
            _RawNews("tagesspiegel"),
            _RawNews(" berlin.de "),
            _RawNews("berlin.de"),
            _RawNews(""),
            _RawNews(None),
        ]
        client = _FakeClient(rows)

        sources = get_unique_news_sources(client)

        self.assertEqual(sources, ["berlin.de", "tagesspiegel"])
        self.assertEqual(client.news_collection.query_params, {"sort": "source"})

    def test_adds_created_filter_when_days_is_provided(self):
        client = _FakeClient([_RawNews("tagesspiegel")])

        get_unique_news_sources(client, days=30)

        query_params = client.news_collection.query_params
        self.assertIsNotNone(query_params)
        assert query_params is not None

        self.assertEqual(query_params["sort"], "source")
        self.assertIn("filter", query_params)
        self.assertRegex(
            query_params["filter"],
            r"^created >= '\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}'$",
        )

    def test_raises_when_days_is_less_than_one(self):
        client = _FakeClient([])

        with self.assertRaises(ValueError):
            get_unique_news_sources(client, days=0)


if __name__ == "__main__":
    unittest.main()
