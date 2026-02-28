import datetime

import myclasses

from .badges import get_badge_by_id

SUPPORTED_NEWS_TYPES = ("google", "rss")
SUPPORTED_NEWS_TYPES_SET = set(SUPPORTED_NEWS_TYPES)

DEFAULT_NEWS_TYPES = ["google", "rss"]


def _validate_news_types(types: list[str]) -> list[str]:
    for news_type in types:
        if news_type not in SUPPORTED_NEWS_TYPES_SET:
            supported_types = ", ".join(SUPPORTED_NEWS_TYPES)
            raise ValueError(
                f"Unsupported news type '{news_type}'. Supported types: {supported_types}."
            )
    return types


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


def get_news_from_day(
    client, date: str, types: list[str] | None = None
) -> list[myclasses.News]:
    try:
        datetime.datetime.strptime(date, "%Y-%m-%d")
    except ValueError as exc:
        raise ValueError("Invalid date format. Please use 'YYYY-MM-DD'.") from exc

    if types is None:
        selected_types = DEFAULT_NEWS_TYPES
    else:
        selected_types = _validate_news_types(types)

    raw_days = client.collection("Days").get_full_list(
        query_params={"filter": f"id = '{date}'"}
    )

    news_items: list[myclasses.News] = []
    if selected_types == []:
        return news_items
    for raw_day in raw_days:
        for news_id in raw_day.news:
            news_item = get_news_from_id(client, news_id)
            if (
                selected_types
                and str(getattr(news_item, "type", "")).lower() not in selected_types
            ):
                continue
            news_items.append(news_item)

    return news_items
