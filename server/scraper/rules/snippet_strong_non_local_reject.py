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

NON_LOCAL_HINTS = (
    "international",
    "weltweit",
    "welt",
    "global",
    "deutschlandweit",
    "bundesweit",
    "europa",
    "usa",
    "ukraine",
    "russland",
    "israel",
    "gaza",
    "china",
    "trump",
    "bundestag",
    "bundesregierung",
)

MIN_NON_LOCAL_MATCHES = 2

NON_LOCAL_PATH_HINTS = (
    "/politik/",
    "/welt/",
    "/international/",
    "/wirtschaft/",
    "/sport/",
    "/boerse/",
    "/finanzen/",
    "/promi/",
    "/panorama/",
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


def _has_non_local_path_hint(link: str) -> bool:
    lowered = (link or "").lower()
    return any(hint in lowered for hint in NON_LOCAL_PATH_HINTS)


def snippet_strong_non_local_reject(article: ArticleInput) -> bool | None:
    snippet_text = _snippet_text(article)
    local_matches = _find_matches(snippet_text, LOCAL_TERMS)
    if local_matches:
        return None

    non_local_matches = _find_matches(_title_description(article), NON_LOCAL_HINTS)
    if len(non_local_matches) >= MIN_NON_LOCAL_MATCHES:
        return False

    if _has_non_local_path_hint(article.link) and not local_matches:
        return False

    if "bundesliga" in _normalize(_title_description(article)):
        return False

    return None
