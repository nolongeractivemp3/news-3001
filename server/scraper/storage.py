import datetime
import os

import myclasses
from db import CRUD
from openrouter import report

openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
pocketbase_url = os.getenv("POCKETBASE_URL", "http://pocketbase:8080")
PRESET_TEST_REPORT_TEXT = (
    "<h2>Testbericht</h2>"
    "<p>Dieser Bericht wurde im Testmodus erstellt.</p>"
    "<p>OpenRouter wurde fuer die Berichterstellung nicht verwendet.</p>"
)


def get_database():
    return CRUD.connection(pocketbase_url)


def create_news_record(article, database) -> myclasses.News:
    news = myclasses.News(
        id="",
        type=article.extra.get("type", "google"),
        source=article.source,
        title=article.title,
        description=article.description,
        link=article.link,
        full_text=article.full_text,
    )
    badges = database.getbadgefornews(news, openrouter_api_key)
    badges = [badge for badge in badges if badge is not None]
    news.badges = badges
    return news


def save_news(news: myclasses.News, database) -> str:
    print("  Saving to database...")
    return database.save_news(news)


def _is_testing_mode_enabled() -> bool:
    return os.getenv("SCRAPER_TESTING_MODE", "false").strip().lower() in (
        "1",
        "true",
        "yes",
        "on",
    )


def _create_and_save_testing_report(database) -> myclasses.Report:
    rep = myclasses.Report(text=PRESET_TEST_REPORT_TEXT)
    rep_id = database.create_report(rep)
    rep.id = rep_id
    return rep


def save_day_report(articles: list[myclasses.News], ids: list[str], database):
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    print(f"\n{'=' * 50}")
    print(f"Results: {len(articles)} local articles")

    if ids:
        if _is_testing_mode_enabled():
            print("Testing mode: creating preset report without OpenRouter")
            rep = _create_and_save_testing_report(database)
        else:
            rep = report.create_and_save_report(database, articles)
        print(f"Report saved with ID: {rep.id}")
        day = myclasses.Day(id=date, news=ids, reportid=rep.id)
        database.save_day(day)
        print(f"Day saved with {len(ids)} local articles")
    else:
        print("No articles found - skipping report generation")
