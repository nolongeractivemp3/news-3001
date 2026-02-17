from .enrichment import enrich_scrape_content
from .fetchers import fetch_google_results, fetch_rss_fallback_results
from .filters import filter_content_locality, filter_snippet_locality
from .models import ArticleInput
from .rules import first_rule_decision
from .storage import create_news_record, get_database, save_day_report, save_news

RSS_FALLBACK_COUNT = 5


def run_scraper(min_filtered_results: int = 3):
    database = get_database()
    articles = fetch_google_results()

    filtered_articles: list[ArticleInput] = []

    for article in articles:
        print(f"\n--- Checking: {article.title} ---")

        enriched = enrich_scrape_content(article)
        if not enriched:
            continue

        rule_result = first_rule_decision(enriched)
        if rule_result is False:
            continue
        if rule_result is None:
            if not filter_snippet_locality(enriched):
                continue

        if not filter_content_locality(enriched):
            continue

        filtered_articles.append(enriched)

    strict_google_count = len(filtered_articles)
    fallback_used = strict_google_count < min_filtered_results
    rss_added = 0
    articles_to_save = list(filtered_articles)

    if fallback_used:
        print(
            f"\nOnly {strict_google_count} articles passed filter (min: {min_filtered_results})"
        )
        print(f"Adding {RSS_FALLBACK_COUNT} RSS fallback articles...")

        rss_articles = fetch_rss_fallback_results(limit=RSS_FALLBACK_COUNT)
        for article in rss_articles:
            print(f"\n--- RSS fallback: {article.title} ---")
            enriched = enrich_scrape_content(article)
            if not enriched:
                continue
            articles_to_save.append(enriched)
            rss_added += 1

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
        "strict_google_count": strict_google_count,
        "fallback_used": fallback_used,
        "rss_added": rss_added,
        "article_ids": saved_ids,
    }
