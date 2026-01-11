import datetime
from sqlite3.dbapi2 import Time

import feedparser
import tldextract
from bs4 import BeautifulSoup as bs

from myclasses import News

url = "https://www.google.de/alerts/feeds/17016683277093386427/7293694784079144231"


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
    feed = feedparser.parse(url)
    news = []
    rawnews = feed.items().mapping["entries"]
    for i in range(len(rawnews)):
        if check_date(rawnews[i].published):
            real_link = extract_real_url(rawnews[i].link)
            news.append(
                News(
                    full_text="",
                    type="rss",
                    source=str(tldextract.extract(real_link).domain.capitalize()),
                    title=bs(rawnews[i].title, "html.parser").get_text(),
                    description=bs(
                        rawnews[i].content[0]["value"], "html.parser"
                    ).get_text(),
                    link=real_link,
                    id=rawnews[i].published,
                )
            )
        print(rawnews[i])
    return news


if __name__ == "__main__":
    rss_feed = get_rss_feed()
