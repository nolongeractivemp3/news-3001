from __future__ import annotations

import os

from rapidfuzz import fuzz, process

from db import CRUD

from ..models import ArticleInput

SIMILARITY_THRESHOLD = 96
SOURCE_LOOKBACK_DAYS = 30
_KNOWN_SOURCES: dict[str, str] = {}
_SOURCES_INITIALIZED = False


def _normalize_source_name(source: str) -> str:
    raw_source = (source or "").strip().lower()
    if not raw_source:
        return ""
    normalized = "".join(char if char.isalnum() else " " for char in raw_source)
    return " ".join(normalized.split())


def _remember_source(source: str) -> None:
    cleaned_source = (source or "").strip()
    if not cleaned_source:
        return
    normalized = _normalize_source_name(cleaned_source)
    if not normalized:
        return
    _KNOWN_SOURCES.setdefault(normalized, cleaned_source)


def _load_sources_once() -> None:
    global _SOURCES_INITIALIZED
    if _SOURCES_INITIALIZED:
        return
    _SOURCES_INITIALIZED = True

    pocketbase_url = os.getenv("POCKETBASE_URL", "").strip()
    if not pocketbase_url:
        return

    try:
        database = CRUD.connection(pocketbase_url)
        known_sources = database.get_unique_news_sources(days=SOURCE_LOOKBACK_DAYS)
    except Exception:
        return

    for source in known_sources:
        _remember_source(source)


def rule(article: ArticleInput) -> bool | None:
    incoming_source = (article.source or "").strip()
    if not incoming_source:
        return None

    _load_sources_once()

    normalized_incoming = _normalize_source_name(incoming_source)
    if not normalized_incoming:
        return None

    if _KNOWN_SOURCES:
        match = process.extractOne(
            normalized_incoming,
            list(_KNOWN_SOURCES.keys()),
            scorer=fuzz.ratio,
            score_cutoff=SIMILARITY_THRESHOLD,
        )
        if match:
            canonical_key, _, _ = match
            canonical_source = _KNOWN_SOURCES.get(canonical_key)
            if canonical_source:
                article.source = canonical_source
                return None

    _remember_source(incoming_source)
    return None
