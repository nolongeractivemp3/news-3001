import datetime
from sqlite3.dbapi2 import Time

import feedparser
import tldextract
from bs4 import BeautifulSoup as bs

from myclasses import News

url = "https://www.google.de/alerts/feeds/17016683277093386427/7293694784079144231"


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
            news.append(
                News(
                    str(tldextract.extract(rawnews[i].link).domain.capitalize()),
                    bs(rawnews[i].title, "html.parser").get_text(),
                    bs(rawnews[i].content[0]["value"], "html.parser").get_text(),
                    rawnews[i].link,
                    rawnews[i].published,
                )
            )
        print(rawnews[i])
    return news


if __name__ == "__main__":
    rss_feed = get_rss_feed()
