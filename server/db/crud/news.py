import datetime

import myclasses

from .badges import get_badge_by_id


def save_news(client, news: myclasses.News) -> str:
    return client.collection("news").create(news.tojson(True)).id


def get_news_from_id(client, news_id: str) -> myclasses.News:
    rawnews = client.collection("news").get_one(news_id)
    badge_ids = getattr(rawnews, "badges", []) or []
    badges = [get_badge_by_id(client, badge_id) for badge_id in badge_ids]
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


def get_news_from_day(client, date: str) -> list[myclasses.News]:
    try:
        datetime.datetime.strptime(date, "%Y-%m-%d")
    except ValueError as exc:
        raise ValueError("Invalid date format. Please use 'YYYY-MM-DD'.") from exc

    raw_days = client.collection("Days").get_full_list(
        query_params={"filter": f"id = '{date}'"}
    )

    news_items: list[myclasses.News] = []
    for raw_day in raw_days:
        for news_id in raw_day.news:
            news_items.append(get_news_from_id(client, news_id))

    return news_items
