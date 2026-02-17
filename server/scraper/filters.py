import os

import content_scraper

from .models import ArticleInput

openrouter_api_key = os.getenv("OPENROUTER_API_KEY")


def filter_snippet_locality(article: ArticleInput) -> bool:
    is_local = content_scraper.check_snippet_locality(
        article.description, article.link, openrouter_api_key
    )
    if not is_local:
        print("  Snippet check: Not local (skipping)")
        return False
    print("  Snippet check: Possibly local")
    return True


def filter_content_locality(article: ArticleInput) -> bool:
    print("  Deep check: Asking AI...")
    is_local = content_scraper.check_full_content_locality(
        article.full_text, openrouter_api_key
    )
    if not is_local:
        return False
    print("  Confirmed local!")
    return True
