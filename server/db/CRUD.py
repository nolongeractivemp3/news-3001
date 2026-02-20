import myclasses

from db.crud.badges import get_all_badges, get_badge_by_id, get_badges_for_news
from db.crud.client import create_authenticated_client
from db.crud.days import save_day
from db.crud.news import get_news_from_day, get_news_from_id, save_news
from db.crud.reports import create_report, get_report_from_day, get_todays_report


class connection:
    def __init__(self, url: str):
        self.client = create_authenticated_client(url)

    def save_news(self, news: myclasses.News) -> str:
        return save_news(self.client, news)

    def save_day(self, day: myclasses.Day) -> str:
        return save_day(self.client, day)

    def create_report(self, report: myclasses.Report) -> str:
        return create_report(self.client, report)

    def get_badge_by_id(self, badge_id: str) -> myclasses.Badge:
        return get_badge_by_id(self.client, badge_id)

    def get_news_from_id(self, news_id: str) -> myclasses.News:
        return get_news_from_id(self.client, news_id)

    def getallbadges(self) -> list[myclasses.Badge]:
        return get_all_badges(self.client)

    def getbadgefornews(self, news: myclasses.News, key: str):
        return get_badges_for_news(self.client, news, key)

    def get_todays_report(self) -> myclasses.Report:
        return get_todays_report(self.client)

    def get_report_from_day(self, date: str) -> myclasses.Report:
        return get_report_from_day(self.client, date)

    def get_news_from_day(self, date: str) -> list[myclasses.News]:
        return get_news_from_day(self.client, date)

__all__ = ["connection"]
