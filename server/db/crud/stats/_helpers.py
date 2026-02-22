import datetime
import json
from collections import Counter
from dataclasses import dataclass

MAX_DAYS_WINDOW = 365


@dataclass(frozen=True)
class NewsRow:
    id: str
    source: str
    article_type: str
    tags: list[str]


def parse_date(date_string: str) -> datetime.date:
    try:
        return datetime.datetime.strptime(date_string, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("Invalid date format. Use 'YYYY-MM-DD'.")


def validate_days(days: int) -> int:
    if not 1 <= days <= MAX_DAYS_WINDOW:
        raise ValueError(f"days must be between 1 and {MAX_DAYS_WINDOW}.")
    return days


def to_string_list(value) -> list[str]:
    if value is None:
        return []

    if isinstance(value, str):
        return _parse_string_to_list(value)

    if isinstance(value, (list, tuple, set)):
        return [str(item) for item in value if item]

    return []


def _parse_string_to_list(value: str) -> list[str]:
    if value == "":
        return []

    try:
        parsed = json.loads(value)
        if isinstance(parsed, list):
            return [str(item) for item in parsed if item]
        return []
    except json.JSONDecodeError:
        return [value]


def sort_counter_by_count(counter: Counter, key_name: str) -> list[dict]:
    sorted_items = sorted(counter.items(), key=lambda item: (-item[1], item[0]))
    return [{key_name: key, "count": count} for key, count in sorted_items]


def calculate_average(total: int, count: int) -> float:
    return round(total / count, 2) if count > 0 else 0.0
