import datetime
import os

from serpapi import search
from rss import get_rss_feed

from .models import ArticleInput

serpapi_api_key = os.getenv("SERPAPI_API_KEY")


def fetch_google_results() -> list[ArticleInput]:
    yesterdate = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime(
        "%Y-%m-%d"
    )
    query = f"köpenick news after:{yesterdate}"
    print(query)

    params = {
        "api_key": serpapi_api_key,
        "engine": "google",
        "q": query,
        "google_domain": "google.com",
    }

    searchy = search(params)
    results = searchy.as_dict()
    organic = results.get("organic_results", [])
    print("Found", len(organic), "results")

    articles = []
    for item in organic:
        articles.append(
            ArticleInput(
                source=item.get("source", ""),
                title=item.get("title", ""),
                description=item.get("snippet", ""),
                link=item.get("link", ""),
                extra={"original": item},
            )
        )
    return articles


def fetch_rss_fallback_results(limit: int = 5) -> list[ArticleInput]:
    rss_news = get_rss_feed()
    print("Found", len(rss_news), "rss results")

    articles = []
    for item in rss_news[:limit]:
        articles.append(
            ArticleInput(
                source=item.source,
                title=item.title,
                description=item.description,
                link=item.link,
                extra={
                    "type": "rss",
                    "original": {
                        "id": item.id,
                        "type": item.type,
                    },
                },
            )
        )
    print("Using", len(articles), "rss fallback results")
    return articles
