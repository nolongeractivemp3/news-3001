from __future__ import annotations

from ..models import ArticleInput

LOCAL_TERMS = (
    "kopenick",
    "koepenick",
    "treptow",
    "treptow kopenick",
    "treptow koepenick",
    "friedrichshagen",
    "muggelheim",
    "mueggelheim",
    "grunau",
    "gruenau",
    "rahnsdorf",
    "schmockwitz",
    "adlershof",
    "oberschoeneweide",
    "niederschoeneweide",
)

MIN_LOCAL_MATCHES_STRONG = 1

LOCAL_PATH_HINTS = (
    "treptow-koepenick",
    "treptow_koepenick",
    "treptowkoepenick",
    "bezirke/treptow",
    "bezirk/treptow",
    "kopenick",
    "koepenick",
    "friedrichshagen",
    "mueggelheim",
    "muggelheim",
    "gruenau",
    "grunau",
    "rahnsdorf",
    "schmockwitz",
)


def _normalize(text: str) -> str:
    normalized = (text or "").lower()
    normalized = (
        normalized.replace("ä", "ae")
        .replace("ö", "oe")
        .replace("ü", "ue")
        .replace("ß", "ss")
    )
    return " " + normalized.replace("-", " ").replace("/", " ") + " "


def _find_matches(text: str, terms: tuple[str, ...]) -> list[str]:
    normalized_text = _normalize(text)
    matches = [term for term in terms if f" {term} " in normalized_text]
    return sorted(set(matches))


def _snippet_text(article: ArticleInput) -> str:
    return " ".join([article.title, article.description, article.link])


def _title_description(article: ArticleInput) -> str:
    return " ".join([article.title, article.description])


def _has_local_path_hint(link: str) -> bool:
    lowered = (link or "").lower()
    return any(hint in lowered for hint in LOCAL_PATH_HINTS)


def snippet_local_keyword_pass(article: ArticleInput) -> bool | None:
    snippet_matches = _find_matches(_snippet_text(article), LOCAL_TERMS)
    if len(snippet_matches) >= MIN_LOCAL_MATCHES_STRONG:
        return True

    text_matches = _find_matches(_title_description(article), LOCAL_TERMS)
    if text_matches and _has_local_path_hint(article.link):
        return True

    if text_matches and "bezirke" in _normalize(article.link):
        return True

    return None
