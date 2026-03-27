import datetime
import json
from collections import Counter
from dataclasses import dataclass

MAX_DAYS_WINDOW = 365
DEFAULT_DAYS_WINDOW = 30


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


def resolve_date_range(
    start_date_string: str | None = None,
    end_date_string: str | None = None,
) -> tuple[datetime.date, datetime.date]:
    if start_date_string is None and end_date_string is None:
        end_date = datetime.date.today()
        start_date = end_date - datetime.timedelta(days=DEFAULT_DAYS_WINDOW - 1)
        return start_date, end_date

    if start_date_string is None or end_date_string is None:
        raise ValueError("Both start_date and end_date are required together.")

    start_date = parse_date(start_date_string)
    end_date = parse_date(end_date_string)

    if start_date > end_date:
        raise ValueError("start_date must be on or before end_date.")

    window_days = (end_date - start_date).days + 1
    if window_days < 1 or window_days > MAX_DAYS_WINDOW:
        raise ValueError(
            f"Date range must be between 1 and {MAX_DAYS_WINDOW} days inclusive."
        )

    return start_date, end_date


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
