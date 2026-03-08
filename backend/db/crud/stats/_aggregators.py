from collections import Counter

from ._helpers import NewsRow, sort_counter_by_count, to_string_list
from ._queries import load_news_row


def build_day_stats(client, raw_day, cache: dict[str, NewsRow]) -> dict:
    day_id, news_ids, report_id = _extract_day_fields(raw_day)
    counts = _count_articles(client, news_ids, cache)

    return {
        "date": day_id,
        "report_id": report_id,
        "news_ids_count": len(news_ids),
        "article_count": counts["article_count"],
        "untagged_article_count": counts["untagged_count"],
        "missing_news_ids": counts["missing_news_ids"],
        "tag_counts": sort_counter_by_count(counts["tag_counts"], "tag"),
        "source_counts": sort_counter_by_count(counts["source_counts"], "source"),
        "type_counts": sort_counter_by_count(counts["type_counts"], "type"),
    }


def _extract_day_fields(raw_day) -> tuple[str, list[str], str]:
    day_id = str(getattr(raw_day, "id", ""))
    news_ids = to_string_list(getattr(raw_day, "news", []))
    report_id = str(getattr(raw_day, "report", "") or "")
    return day_id, news_ids, report_id


def _count_articles(client, news_ids: list[str], cache: dict[str, NewsRow]) -> dict:
    tag_counts = Counter()
    source_counts = Counter()
    type_counts = Counter()
    missing_news_ids = []
    article_count = 0
    untagged_count = 0

    for news_id in news_ids:
        row = load_news_row(client, news_id, cache)
        if row is None:
            missing_news_ids.append(news_id)
            continue

        article_count += 1
        source_counts[row.source] += 1
        type_counts[row.article_type] += 1

        if row.tags:
            tag_counts.update(row.tags)
        else:
            untagged_count += 1

    return {
        "tag_counts": tag_counts,
        "source_counts": source_counts,
        "type_counts": type_counts,
        "missing_news_ids": missing_news_ids,
        "article_count": article_count,
        "untagged_count": untagged_count,
    }


def aggregate_totals(day_stats: list[dict]) -> dict:
    total_articles = 0
    total_tag_assignments = 0
    tag_totals = Counter()
    source_totals = Counter()
    type_totals = Counter()

    for day in day_stats:
        total_articles += day["article_count"]

        for tag_entry in day["tag_counts"]:
            total_tag_assignments += tag_entry["count"]
            tag_totals[tag_entry["tag"]] += tag_entry["count"]

        for source_entry in day["source_counts"]:
            source_totals[source_entry["source"]] += source_entry["count"]

        for type_entry in day["type_counts"]:
            type_totals[type_entry["type"]] += type_entry["count"]

    return {
        "total_articles": total_articles,
        "total_tag_assignments": total_tag_assignments,
        "tag_totals": tag_totals,
        "source_totals": source_totals,
        "type_totals": type_totals,
    }


def build_daily_entry(
    client, raw_day, cache: dict[str, NewsRow], badge_names: dict[str, str]
) -> dict:
    stats = build_day_stats(client, raw_day, cache)
    tag_counts = [
        {"tag": badge_names.get(entry["tag"], entry["tag"]), "count": entry["count"]}
        for entry in stats["tag_counts"]
    ]
    return {
        "date": stats["date"],
        "article_count": stats["article_count"],
        "untagged_article_count": stats["untagged_article_count"],
        "tag_counts": tag_counts,
        "source_counts": stats["source_counts"],
    }
