import datetime
import os

from serpapi import search

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
