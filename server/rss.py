import feedparser
from bs4 import BeautifulSoup as bs

from objects import News

url = "https://www.google.de/alerts/feeds/17016683277093386427/7293694784079144231"


# def get_rss_feed() -> list[News]:
def get_rss_feed():
    feed = feedparser.parse(url)
    news = []
    rawnews = feed.items().mapping["entries"]
    for i in range(len(rawnews)):
        print()
        news.append(
            News(
                "RSS feed",
                bs(rawnews[i].title, "html.parser").get_text(),
                bs(rawnews[i].content[0]["value"], "html.parser").get_text(),
                rawnews[i].link,
            )
        )
    return news


if __name__ == "__main__":
    get_rss_feed()
