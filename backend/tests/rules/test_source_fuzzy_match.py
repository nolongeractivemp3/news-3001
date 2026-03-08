from __future__ import annotations

from pathlib import Path
import sys
import unittest
from unittest.mock import patch

# Allow running this test directly from any working directory.
SERVER_ROOT = Path(__file__).resolve().parents[2]
if str(SERVER_ROOT) not in sys.path:
    sys.path.insert(0, str(SERVER_ROOT))

from scraper.models import ArticleInput
from scraper.rules import source_fuzzy_match


def make_article(source: str) -> ArticleInput:
    return ArticleInput(
        source=source,
        title="Treptow district update",
        description="",
        link="https://example.com/article/1",
        full_text="",
        extra={},
    )


class SourceFuzzyMatchRuleTests(unittest.TestCase):
    def setUp(self):
        source_fuzzy_match._KNOWN_SOURCES.clear()
        source_fuzzy_match._SOURCES_INITIALIZED = True

    def test_replaces_source_when_very_similar(self):
        canonical_source = "Berliner Morgenpost"
        source_fuzzy_match._remember_source(canonical_source)

        article = make_article("Berliner Morgen Post")
        result = source_fuzzy_match.rule(article)

        self.assertIsNone(result)
        self.assertEqual(article.source, canonical_source)

    def test_keeps_source_when_not_similar(self):
        source_fuzzy_match._remember_source("Tagesspiegel")

        article = make_article("Berliner Zeitung")
        source_fuzzy_match.rule(article)

        self.assertEqual(article.source, "Berliner Zeitung")

    def test_loads_recent_sources_with_30_day_window(self):
        class FakeDatabase:
            def __init__(self):
                self.days_args = []

            def get_unique_news_sources(self, days=None):
                self.days_args.append(days)
                return ["Tagesspiegel"]

        fake_db = FakeDatabase()
        source_fuzzy_match._SOURCES_INITIALIZED = False

        with (
            patch.dict(
                "os.environ", {"POCKETBASE_URL": "http://localhost"}, clear=False
            ),
            patch(
                "scraper.rules.source_fuzzy_match.CRUD.connection", return_value=fake_db
            ),
        ):
            source_fuzzy_match.rule(make_article("Tagesspiegel"))

        self.assertEqual(fake_db.days_args, [30])


if __name__ == "__main__":
    unittest.main()
