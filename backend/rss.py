import datetime
import os

import feedparser
import tldextract
from bs4 import BeautifulSoup as bs

from myclasses import News

DEFAULT_GOOGLE_ALERTS_FEED_URL = (
    "https://www.google.de/alerts/feeds/17016683277093386427/7293694784079144231"
)


def _get_rss_feed_url() -> str:
    value = os.getenv("SCRAPER_RSS_FEED_URL", DEFAULT_GOOGLE_ALERTS_FEED_URL).strip()
    return value or DEFAULT_GOOGLE_ALERTS_FEED_URL


def extract_real_url(google_url: str) -> str:
    """
    Extract the real URL from a Google redirect link using string splitting.
    """
    if "google.com/url" in google_url or "google.de/url" in google_url:
        if "url=" in google_url:
            # Split on 'url=' and take everything after it
            real_url = google_url.split("url=")[1]
            # Remove any trailing parameters (everything after &)
            if "&" in real_url:
                real_url = real_url.split("&")[0]
            return real_url
    return google_url


def check_date(date: str):
    print(date)
    x = date.split("T")
    dates = x[0]
    times = x[1][: len(x[1]) - 1]
    y = datetime.datetime.strptime(f"{dates} {times}", "%Y-%m-%d %H:%M:%S")
    yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
    print(y)
    print(yesterday)
    if y > yesterday:
        return True
    return False


def get_rss_feed() -> list[News]:
    feed = feedparser.parse(_get_rss_feed_url())
    news = []
    rawnews = feed.entries
    for item in rawnews:
        if check_date(item.published):
            real_link = extract_real_url(item.link)
            description_html = ""
            if getattr(item, "content", None):
                description_html = item.content[0].get("value", "")
            elif getattr(item, "summary", None):
                description_html = item.summary

            news.append(
                News(
                    full_text="",
                    type="rss",
                    source=str(tldextract.extract(real_link).domain.capitalize()),
                    title=bs(item.title, "html.parser").get_text(),
                    description=bs(description_html, "html.parser").get_text(),
                    link=real_link,
                    id=f"{item.published}:{real_link}",
                )
            )
        print(item)
    return news


if __name__ == "__main__":
    rss_feed = get_rss_feed()
