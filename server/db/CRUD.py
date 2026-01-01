import datetime

import pocketbase
from typing_extensions import Dict

import myclasses


class connection:
    def __init__(self, url: str):
        self.client = pocketbase.Client(url)

    def save_news(self, news: myclasses.News) -> str:
        # news.todict()
        return self.client.collection("news").create(news.todict()).id

    def save_day(self, day: myclasses.Day) -> str:
        return (
            self.client.collection("days")
            .create({"date": day.date, "News": day.NewsIds})
            .id
        )

    def get_news_from_id(self, id: str) -> myclasses.News:
        rawnews = self.client.collection("news").get_one(id)
        return myclasses.News(
            rawnews.source,
            rawnews.title,
            rawnews.description,
            rawnews.link,
            rawnews.date,
        )

    def get_news(
        self,
    ) -> list[myclasses.News]:
        rawnews = self.client.collection("news").get_full_list(
            query_params={
                "sort": "-date",  # The minus '-' means DESCENDING (last ones first)
                "filter": "date != ''",  # Optional: only if title isn't empty
            }
        )
        news = []
        for rawnew in rawnews:
            print(rawnew)
            news.append(
                myclasses.News(
                    rawnew.source,
                    rawnew.title,
                    rawnew.description,
                    rawnew.link,
                    rawnew.date,
                )
            )

            print(rawnew.source)
        return news

    def get_news_from_day(self, date: str) -> list[myclasses.News]:
        rawday = self.client.collection("days").get_full_list(
            batch=1, query_params={"filter": f"date = '{date}'"}
        )
        news = []
        for rawday in rawday:
            for newsid in rawday.news:
                news.append(self.get_news_from_id(newsid))
                print(self.get_news_from_id(newsid))  # ??
        return news


if __name__ == "__main__":
    news = myclasses.News("Source", "Title", "description", "water", "2023-01-01 00:00")
    save_news(news)
