import datetime

from ._aggregators import aggregate_totals, build_daily_entry, build_day_stats
from ._helpers import (
    calculate_average,
    parse_date,
    sort_counter_by_count,
    validate_days,
)
from ._queries import get_badge_name_map, get_day_by_date, get_days_in_window


def get_day_stats(client, date: str) -> dict:
    parse_date(date)
    raw_days = get_day_by_date(client, date)

    if not raw_days:
        raise ValueError(f"No day found for date: {date}")

    return build_day_stats(client, raw_days[0], {})


def get_tag_usage_by_day(client, days: int = 30) -> dict:
    days = validate_days(days)
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=days - 1)

    raw_days = get_days_in_window(client, start_date, end_date)
    cache = {}
    badge_names = get_badge_name_map(client)
    daily = [
        build_daily_entry(client, raw_day, cache, badge_names) for raw_day in raw_days
    ]

    return {
        "days_requested": days,
        "start_date": str(start_date),
        "end_date": str(end_date),
        "days_with_data": len(daily),
        "daily": daily,
    }


def get_scraper_summary(client, days: int = 30) -> dict:
    days = validate_days(days)
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=days - 1)

    raw_days = get_days_in_window(client, start_date, end_date)
    cache = {}
    day_stats = [build_day_stats(client, raw_day, cache) for raw_day in raw_days]

    totals = aggregate_totals(day_stats)
    average_articles = calculate_average(totals["total_articles"], len(day_stats))

    return {
        "days_requested": days,
        "start_date": str(start_date),
        "end_date": str(end_date),
        "days_with_data": len(day_stats),
        "total_articles": totals["total_articles"],
        "average_articles_per_day": average_articles,
        "total_tag_assignments": totals["total_tag_assignments"],
        "top_tags": sort_counter_by_count(totals["tag_totals"], "tag")[:10],
        "top_sources": sort_counter_by_count(totals["source_totals"], "source")[:10],
        "top_types": sort_counter_by_count(totals["type_totals"], "type")[:10],
        "daily_article_counts": [
            {"date": day["date"], "count": day["article_count"]} for day in day_stats
        ],
    }
