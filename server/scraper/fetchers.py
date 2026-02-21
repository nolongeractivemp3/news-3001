import datetime
import os

from rss import get_rss_feed

from .models import ArticleInput


def fetch_google_results() -> list[ArticleInput]:
    raise RuntimeError("tried to scrape live news")
    try:
        from serpapi import search
    except ImportError as exc:
        raise RuntimeError(
            "Google mode requires the 'serpapi' package to be installed."
        ) from exc

    serpapi_api_key = os.getenv("SERPAPI_API_KEY")
    if not serpapi_api_key:
        raise RuntimeError(
            "Missing SERPAPI_API_KEY environment variable for Google mode."
        )

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


def fetch_test_articles() -> list[ArticleInput]:
    articles = [
        ArticleInput(
            source="Manual Berlin Feed",
            title="Köpenick district library starts evening reading program",
            description=(
                "Treptow-Köpenick residents can join weekly reading sessions "
                "at the district library."
            ),
            link="https://manual.test/koepenick/library-evening-program",
            full_text=(
                "The district office of Treptow-Koepenick announced a new evening "
                "reading program at the Koepenick central library. Local families "
                "from nearby neighborhoods are invited to attend sessions every "
                "Thursday."
            ),
            extra={"type": "manual_test", "original": {"type": "manual", "index": 1}},
        ),
        ArticleInput(
            source="Manual Berlin Feed",
            title="Treptow-Köpenick opens new bike lane near S-Bahn",
            description=(
                "A new bike corridor improves commuter access between Adlershof "
                "and Köpenick."
            ),
            link="https://manual.test/treptow-koepenick/new-bike-lane",
            full_text=(
                "The borough administration in Treptow-Koepenick opened a new bike "
                "lane connecting major commuter routes. The route runs near local "
                "schools and transit stops and is focused on district-level traffic "
                "safety."
            ),
            extra={"type": "manual_test", "original": {"type": "manual", "index": 2}},
        ),
        ArticleInput(
            source="Manual Berlin Feed",
            title="Köpenick global sports partnership announced",
            description="District club leaders discussed an international cooperation project.",
            link="https://manual.test/koepenick/global-partnership",
            full_text=(
                "A sports organization in Koepenick announced a global partnership "
                "program with clubs outside Berlin. The project focuses on exchange "
                "events and long-term sponsorship opportunities."
            ),
            extra={"type": "manual_test", "original": {"type": "manual", "index": 3}},
        ),
    ]
    print("Using", len(articles), "manual test results")
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
