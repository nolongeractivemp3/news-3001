import datetime
import time

from rapidfuzz import fuzz

import myclasses

from .badges import get_badge_by_id

_news_cache: tuple[float, list] = (0, [])


def _get_all_news_cached(client, ttl: int = 300) -> list:
    global _news_cache
    now = time.time()
    if now - _news_cache[0] > ttl:
        raw_news = client.collection("news").get_full_list()
        _news_cache = (now, raw_news)
    return _news_cache[1]


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


def _raw_to_news(client, raw_item) -> myclasses.News:
    badge_ids = getattr(raw_item, "badges", []) or []
    badges = [get_badge_by_id(client, badge_id) for badge_id in badge_ids]
    return myclasses.News(
        raw_item.id,
        raw_item.type,
        raw_item.title,
        raw_item.description,
        raw_item.full_text,
        raw_item.source,
        raw_item.link,
        badges,
    )


def get_recent_news(
    client, limit: int = 30, page: int = 1
) -> tuple[list[myclasses.News], int]:
    raw_news = _get_all_news_cached(client)
    raw_news = sorted(
        raw_news, key=lambda x: getattr(x, "date", "") or "", reverse=True
    )
    total = len(raw_news)
    offset = (page - 1) * limit
    return [
        _raw_to_news(client, item) for item in raw_news[offset : offset + limit]
    ], total


def search_news(
    client, query: str, limit: int = 30, page: int = 1
) -> tuple[list[myclasses.News], int]:
    if not query or len(query.strip()) < 2:
        return [], 0

    search_term = query.strip().lower()
    words = search_term.split()

    raw_news = _get_all_news_cached(client)

    scored = []
    for item in raw_news:
        title = (item.title or "").lower()
        description = (item.description or "").lower()
        full_text = (item.full_text or "").lower()

        title_ratio = fuzz.token_sort_ratio(search_term, title)
        desc_ratio = fuzz.token_sort_ratio(search_term, description)
        full_ratio = fuzz.token_sort_ratio(search_term, full_text)
        partial = fuzz.partial_ratio(search_term, f"{title} {description}")

        bonus = 0
        for word in words:
            if word in title.split():
                bonus += 25
            elif word in title:
                bonus += 15
            if word in description:
                bonus += 10
            if word in full_text:
                bonus += 5

        best_score = max(title_ratio, desc_ratio, full_ratio, partial) + bonus

        if best_score >= 60:
            scored.append((best_score, item))

    scored.sort(key=lambda x: x[0], reverse=True)
    total = len(scored)
    offset = (page - 1) * limit
    top_items = [item for _, item in scored[offset : offset + limit]]

    return [_raw_to_news(client, item) for item in top_items], total
