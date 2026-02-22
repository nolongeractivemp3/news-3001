import datetime

from ..badges import get_all_badges
from ._helpers import NewsRow, to_string_list


def get_days_in_window(client, start_date: datetime.date, end_date: datetime.date):
    filter_str = f"id >= '{start_date}' && id <= '{end_date}'"
    return client.collection("Days").get_full_list(
        query_params={"filter": filter_str, "sort": "id"}
    )


def get_day_by_date(client, date: str):
    return client.collection("Days").get_full_list(
        query_params={"filter": f"id = '{date}'"}
    )


def load_news_row(client, news_id: str, cache: dict[str, NewsRow]) -> NewsRow | None:
    if news_id in cache:
        return cache[news_id]

    try:
        raw = client.collection("news").get_one(news_id)
    except Exception:
        return None

    row = NewsRow(
        id=str(getattr(raw, "id", news_id)),
        source=str(getattr(raw, "source", "unknown") or "unknown"),
        article_type=str(getattr(raw, "type", "unknown") or "unknown"),
        tags=to_string_list(getattr(raw, "badges", [])),
    )
    cache[news_id] = row
    return row


def get_badge_name_map(client) -> dict[str, str]:
    return {badge.id: badge.name for badge in get_all_badges(client)}
