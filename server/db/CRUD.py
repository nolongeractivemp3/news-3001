import datetime

import pocketbase
from typing_extensions import Dict

import myclasses
from openrouter.badges import get_badges


class connection:
    def __init__(self, url: str):
        self.client = pocketbase.Client(url)
        # Hardcoded credentials as requested
        admin_email = "handyjason053@gmail.com"
        admin_password = "handyjason053@gmail.com"
        self.client.admins.auth_with_password(admin_email, admin_password)

    def save_news(self, news: myclasses.News) -> str:
        data = news.tojson()
        # Get badge IDs from the news object
        return self.client.collection("news").create(data).id

    def save_day(self, day: myclasses.Day) -> str:
        return self.client.collection("days").create(day.tojson()).id

    def create_report(self, report: myclasses.Report) -> str:
        return self.client.collection("report").create(report.tojson()).id

    def get_badge_by_id(self, badge_id: str) -> myclasses.Badge:
        """Fetch a single badge by ID."""
        raw_badge = self.client.collection("badges").get_one(badge_id)
        return myclasses.Badge(
            raw_badge.name, raw_badge.description, raw_badge.id, raw_badge.hexcolor
        )

    def get_news_from_id(self, id: str) -> myclasses.News:
        """Fetch a single news item by ID.
        Args:
            id (str): The ID of the news item to fetch.
        Returns:
            myclasses.News: The news item with the specified ID.
        """
        rawnews = self.client.collection("news").get_one(id)
        # Get badge IDs from the news record and fetch each badge
        badge_ids = getattr(rawnews, "badges", []) or []
        badges = [self.get_badge_by_id(bid) for bid in badge_ids]
        return myclasses.News(
            rawnews.id,
            rawnews.type,
            rawnews.title,
            rawnews.description,
            rawnews.full_text,
            rawnews.source,
            rawnews.link,
            badges,
        )

    def getallbadges(self) -> list[myclasses.Badge]:
        badges = []
        for badge in self.client.collection("badges").get_full_list():
            badges.append(
                myclasses.Badge(badge.name, badge.description, badge.id, badge.hexcolor)
            )
        return badges

    def getbadgefornews(self, news: myclasses.News, key: str):
        return get_badges(news, self.getallbadges(), key)

    def get_todays_report(self) -> myclasses.Report:
        print("Getting today's report...")
        reportid = (
            self.client.collection("Days")
            .get_list(1, query_params={"sort": "-id"})
            .items[0]
            .report
        )
        print(reportid)
        report = self.client.collection("Report").get_one(reportid)
        return myclasses.Report(report.id, report.text)

    def get_news_from_day(self, date: str) -> list[myclasses.News]:
        """Get news from a specific day.
        args:
            date (str): The date in the format 'YYYY-MM-DD'.
        returns:
            list[myclasses.News]: A list of news articles from the specified day.
        """
        print(date)
        rawday = self.client.collection("Days").get_full_list(
            query_params={"filter": f"id = '{date}'"}
        )
        print(rawday)
        news = []
        for rawday in rawday:
            for newsid in rawday.news:
                news.append(self.get_news_from_id(newsid))
                print(self.get_news_from_id(newsid))  # ??

        return news


if __name__ == "__main__":
    news = myclasses.News("Source", "Title", "description", "water", "2023-01-01 00:00")
    save_news(news)
