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


def fetch_test_articles() -> list[ArticleInput]:
    articles = [
        ArticleInput(
            source="Berlin.de",
            title="Feministischer März 2026 in Treptow-Köpenick",
            description=(
                "Im Feministischen März laden auch im Jahr 2026 wieder zahlreiche "
                "Organisationen, Initiativen, Aktivist*innen und die "
                "Gleichstellungsbeauftragte zu ..."
            ),
            link="https://www.berlin.de/ba-treptow-koepenick/aktuelles/pressemitteilungen/2026/pressemitteilung.1640109.php",
            extra={
                "type": "manual_test",
                "original": {"id": "8yki9112ul3slub", "type": "google"},
            },
        ),
        ArticleInput(
            source="B.Z. – Die Stimme Berlins",
            title="Treptow-Köpenick - Berlin",
            description=(
                "Aktuelle Nachrichten aus Treptow-Köpenick. News zu Politik, "
                "Wirtschaft, Sport und Kultur sowie aktuelle Polizeimeldungen "
                "aus Berlin auf BZ.de."
            ),
            link="https://www.bz-berlin.de/berlin/treptow-koepenick",
            extra={
                "type": "manual_test",
                "original": {"id": "9n3lu3lh1lew5pe", "type": "google"},
            },
        ),
        ArticleInput(
            source="Berliner Morgenpost",
            title="Berlin: Folge des harten Winters – Deutlich mehr ...",
            description=(
                "Alle entstandenen Straßenschäden zu reparieren, wird lange "
                "dauern. Aus Treptow-Köpenick kommt nun eine deutliche Forderung "
                "an den Senat."
            ),
            link="https://www.morgenpost.de/bezirke/treptow-koepenick/article411195191/folge-des-harten-winters-in-berlin-deutlich-mehr-schlagloecher-als-sonst.html",
            extra={
                "type": "manual_test",
                "original": {"id": "wqpv9icain1mxdo", "type": "google"},
            },
        ),
        ArticleInput(
            source="Tagesspiegel",
            title="Alle Artikel in „Treptow-Köpenick“ vom 10.01.2026",
            description=(
                "Eine Übersicht aller Artikel des Ressorts Treptow-Köpenick vom "
                "10.01.2026 finden Sie in unserem Tagesspiegel Archiv."
            ),
            link="https://www.tagesspiegel.de/berlin/bezirke/treptow-koepenick/archiv/2026/01/10",
            extra={
                "type": "manual_test",
                "original": {"id": "16t7xiu7qw74a6y", "type": "google"},
            },
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
