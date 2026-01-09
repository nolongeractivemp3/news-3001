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
        if news.badges:
            data["badges"] = [badge.id for badge in news.badges]
        print(data)
        return self.client.collection("news").create(data).id

    def save_day(self, day: myclasses.Day) -> str:
        return (
            self.client.collection("days")
            .create({"date": day.date, "News": day.NewsIds, "Report": day.Report})
            .id
        )

    def create_report(self, report: myclasses.Report) -> str:
        return self.client.collection("report").create({"text": report.Summary}).id

    def get_badge_by_id(self, badge_id: str) -> myclasses.Badge:
        """Fetch a single badge by ID."""
        raw_badge = self.client.collection("badges").get_one(badge_id)
        return myclasses.Badge(raw_badge.name, raw_badge.description, raw_badge.id)

    def get_news_from_id(self, id: str) -> myclasses.News:
        rawnews = self.client.collection("news").get_one(id)
        # Get badge IDs from the news record and fetch each badge
        badge_ids = getattr(rawnews, "badges", []) or []
        badges = [self.get_badge_by_id(bid) for bid in badge_ids]
        return myclasses.News(
            rawnews.source,
            rawnews.title,
            rawnews.description,
            rawnews.link,
            rawnews.date,
            # getattr safely gets attribute or returns None if it doesn't exist
            # (for backwards compatibility with old records without full_content)
            getattr(rawnews, "full_content", None),
            badges,
        )

    def getallbadges(self) -> list[myclasses.Badge]:
        badges = []
        for badge in self.client.collection("badges").get_full_list():
            badges.append(myclasses.Badge(badge.name, badge.description, badge.id))
        return badges

    def getbadgefornews(self, news: myclasses.News, key: str):
        return get_badges(news, self.getallbadges(), key)

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
            # Get badge IDs from the news record and fetch each badge
            badge_ids = getattr(rawnew, "badges", []) or []
            badges = [self.get_badge_by_id(bid) for bid in badge_ids]
            news.append(
                myclasses.News(
                    rawnew.source,
                    rawnew.title,
                    rawnew.description,
                    rawnew.link,
                    rawnew.date,
                    # getattr: safely returns None for old records without full_content
                    getattr(rawnew, "full_content", None),
                    badges,
                )
            )

            print(rawnew.source)
        return news

    def get_todays_report(self) -> myclasses.Report:
        reportid = (
            self.client.collection("days")
            .get_list(1, query_params={"sort": "-date"})
            .items[0]
            .report
        )
        report = self.client.collection("report").get_one(reportid)
        return myclasses.Report(report.text)

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
