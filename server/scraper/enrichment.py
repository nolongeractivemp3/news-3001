import content_scraper

from .models import ArticleInput


def enrich_scrape_content(
    article: ArticleInput, use_description_fallback: bool = False
) -> ArticleInput | None:
    print("  Scraping full content...")
    full_content = content_scraper.scrape_article_simple(article.link)
    if not full_content:
        if use_description_fallback:
            fallback_content = (
                article.description or article.title or "No content available."
            )
            print("  Could not scrape content (using description fallback)")
            article.full_text = fallback_content[:4999]
            return article
        print("  Could not scrape content (skipping)")
        return None
    if len(full_content) > 4999:
        print(f"  Cutting content from {len(full_content)} to 4999")
        full_content = full_content[:4999]
    article.full_text = full_content
    return article
