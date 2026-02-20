import datetime
import json
from collections import Counter
from dataclasses import dataclass
from typing import Any

MAX_DAYS_WINDOW = 365


@dataclass(frozen=True)
class _NewsStatsRow:
    id: str
    source: str
    article_type: str
    tags: list[str]


def _parse_date(date: str) -> datetime.date:
    try:
        return datetime.datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError as exc:
        raise ValueError("Invalid date format. Please use 'YYYY-MM-DD'.") from exc


def _validate_days(days: int) -> int:
    if days < 1 or days > MAX_DAYS_WINDOW:
        raise ValueError(f"days must be between 1 and {MAX_DAYS_WINDOW}.")
    return days


def _as_string_list(raw_value: Any) -> list[str]:
    if raw_value is None:
        return []

    if isinstance(raw_value, (list, tuple, set)):
        return [str(item) for item in raw_value if item]

    if isinstance(raw_value, str):
        if raw_value == "":
            return []
        try:
            parsed = json.loads(raw_value)
        except json.JSONDecodeError:
            return [raw_value]
        if isinstance(parsed, list):
            return [str(item) for item in parsed if item]
        return []

    return []


def _counter_to_sorted_items(
    counter: Counter[str], key_name: str
) -> list[dict[str, str | int]]:
    sorted_items = sorted(counter.items(), key=lambda item: (-item[1], item[0]))
    return [{key_name: key, "count": count} for key, count in sorted_items]


def _load_news_row(
    client, news_id: str, cache: dict[str, _NewsStatsRow]
) -> _NewsStatsRow | None:
    if news_id in cache:
        return cache[news_id]

    try:
        raw_news = client.collection("news").get_one(news_id)
    except Exception:
        return None

    row = _NewsStatsRow(
        id=str(getattr(raw_news, "id", news_id)),
        source=str(getattr(raw_news, "source", "unknown") or "unknown"),
        article_type=str(getattr(raw_news, "type", "unknown") or "unknown"),
        tags=_as_string_list(getattr(raw_news, "badges", [])),
    )
    cache[news_id] = row
    return row


def _build_day_stats(client, raw_day: Any, cache: dict[str, _NewsStatsRow]) -> dict[str, Any]:
    day_id = str(getattr(raw_day, "id", ""))
    news_ids = _as_string_list(getattr(raw_day, "news", []))

    tag_counts: Counter[str] = Counter()
    source_counts: Counter[str] = Counter()
    type_counts: Counter[str] = Counter()
    missing_news_ids: list[str] = []

    article_count = 0
    untagged_article_count = 0

    for news_id in news_ids:
        row = _load_news_row(client, news_id, cache)
        if row is None:
            missing_news_ids.append(news_id)
            continue

        article_count += 1
        source_counts[row.source] += 1
        type_counts[row.article_type] += 1
        if row.tags:
            tag_counts.update(row.tags)
        else:
            untagged_article_count += 1

    return {
        "date": day_id,
        "report_id": str(getattr(raw_day, "report", "") or ""),
        "news_ids_count": len(news_ids),
        "article_count": article_count,
        "untagged_article_count": untagged_article_count,
        "missing_news_ids": missing_news_ids,
        "tag_counts": _counter_to_sorted_items(tag_counts, "tag"),
        "source_counts": _counter_to_sorted_items(source_counts, "source"),
        "type_counts": _counter_to_sorted_items(type_counts, "type"),
    }


def _get_days_in_window(client, start_date: datetime.date, end_date: datetime.date):
    filter_query = (
        f"id >= '{start_date.strftime('%Y-%m-%d')}' "
        f"&& id <= '{end_date.strftime('%Y-%m-%d')}'"
    )
    return client.collection("Days").get_full_list(
        query_params={"filter": filter_query, "sort": "id"}
    )


def _build_window_stats(
    client, days: int
) -> tuple[list[dict[str, Any]], datetime.date, datetime.date]:
    normalized_days = _validate_days(days)
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=normalized_days - 1)

    raw_days = _get_days_in_window(client, start_date, end_date)
    cache: dict[str, _NewsStatsRow] = {}
    day_stats = [_build_day_stats(client, raw_day, cache) for raw_day in raw_days]
    return day_stats, start_date, end_date


def get_day_stats(client, date: str) -> dict[str, Any]:
    _parse_date(date)

    raw_days = client.collection("Days").get_full_list(
        query_params={"filter": f"id = '{date}'"}
    )
    if len(raw_days) == 0:
        raise ValueError(f"No day found for date: {date}")

    return _build_day_stats(client, raw_days[0], {})


def get_tag_usage_by_day(client, days: int = 30) -> dict[str, Any]:
    day_stats, start_date, end_date = _build_window_stats(client, days)
    daily = [
        {
            "date": day["date"],
            "article_count": day["article_count"],
            "untagged_article_count": day["untagged_article_count"],
            "tag_counts": day["tag_counts"],
            "source_counts": day["source_counts"],
        }
        for day in day_stats
    ]

    return {
        "days_requested": days,
        "start_date": start_date.strftime("%Y-%m-%d"),
        "end_date": end_date.strftime("%Y-%m-%d"),
        "days_with_data": len(daily),
        "daily": daily,
    }


def get_scraper_summary(client, days: int = 30) -> dict[str, Any]:
    day_stats, start_date, end_date = _build_window_stats(client, days)

    total_articles = 0
    total_tag_assignments = 0
    tag_totals: Counter[str] = Counter()
    source_totals: Counter[str] = Counter()
    type_totals: Counter[str] = Counter()

    for day in day_stats:
        total_articles += int(day["article_count"])
        total_tag_assignments += sum(
            int(tag_entry["count"]) for tag_entry in day["tag_counts"]
        )

        for tag_entry in day["tag_counts"]:
            tag_totals[str(tag_entry["tag"])] += int(tag_entry["count"])
        for source_entry in day["source_counts"]:
            source_totals[str(source_entry["source"])] += int(source_entry["count"])
        for type_entry in day["type_counts"]:
            type_totals[str(type_entry["type"])] += int(type_entry["count"])

    average_articles_per_day = (
        round(total_articles / len(day_stats), 2) if len(day_stats) > 0 else 0.0
    )

    return {
        "days_requested": days,
        "start_date": start_date.strftime("%Y-%m-%d"),
        "end_date": end_date.strftime("%Y-%m-%d"),
        "days_with_data": len(day_stats),
        "total_articles": total_articles,
        "average_articles_per_day": average_articles_per_day,
        "total_tag_assignments": total_tag_assignments,
        "top_tags": _counter_to_sorted_items(tag_totals, "tag")[:10],
        "top_sources": _counter_to_sorted_items(source_totals, "source")[:10],
        "top_types": _counter_to_sorted_items(type_totals, "type")[:10],
        "daily_article_counts": [
            {"date": day["date"], "count": day["article_count"]} for day in day_stats
        ],
    }
