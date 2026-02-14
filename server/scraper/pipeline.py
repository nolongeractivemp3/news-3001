from .enrichment import enrich_scrape_content
from .fetchers import fetch_google_results
from .filters import filter_content_locality, filter_snippet_locality
from .models import ArticleInput
from .storage import create_news_record, get_database, save_day_report, save_news


def run_scraper():
    database = get_database()
    articles = fetch_google_results()

    saved_articles = []
    saved_ids = []

    for article in articles:
        print(f"\n--- Checking: {article.title} ---")

        article = enrich_scrape_content(article)
        if not article:
            continue

        if not filter_snippet_locality(article):
            continue

        if not filter_content_locality(article):
            continue

        news = create_news_record(article, database)
        news_id = save_news(news, database)
        saved_ids.append(news_id)
        saved_articles.append(news)

    save_day_report(saved_articles, saved_ids, database)

    return {
        "total_results": len(articles),
        "saved_articles": len(saved_articles),
        "article_ids": saved_ids,
    }
