from .enrichment import enrich_scrape_content
from .fetchers import fetch_google_results
from .filters import filter_content_locality, filter_snippet_locality
from .models import ArticleInput
from .storage import create_news_record, get_database, save_day_report, save_news


def run_scraper(min_filtered_results: int = 3):
    database = get_database()
    articles = fetch_google_results()

    filtered_articles = []
    all_enriched_articles = []

    for article in articles:
        print(f"\n--- Checking: {article.title} ---")

        enriched = enrich_scrape_content(article)
        if not enriched:
            continue

        all_enriched_articles.append(enriched)

        if not filter_snippet_locality(enriched):
            continue

        if not filter_content_locality(enriched):
            continue

        filtered_articles.append(enriched)

    if len(filtered_articles) < min_filtered_results:
        print(
            f"\nOnly {len(filtered_articles)} articles passed filter (min: {min_filtered_results})"
        )
        print("Saving all enriched articles instead...")
        articles_to_save = all_enriched_articles
    else:
        articles_to_save = filtered_articles

    saved_articles = []
    saved_ids = []

    for article in articles_to_save:
        news = create_news_record(article, database)
        news_id = save_news(news, database)
        saved_ids.append(news_id)
        saved_articles.append(news)

    save_day_report(saved_articles, saved_ids, database)

    return {
        "total_results": len(articles),
        "saved_articles": len(saved_articles),
        "filtered_articles": len(filtered_articles),
        "article_ids": saved_ids,
    }
