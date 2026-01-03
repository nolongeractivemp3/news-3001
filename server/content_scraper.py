"""
Content Scraper Module

A reusable module for extracting article content from URLs.
Can be used for news articles, blog posts, or any web content.
"""

from dataclasses import dataclass
from typing import Optional

import trafilatura


@dataclass
class ScrapedContent:
    """Container for scraped content results."""

    url: str
    content: Optional[str]
    title: Optional[str]
    success: bool
    error: Optional[str] = None


def scrape_article(url: str, timeout: int = 10) -> ScrapedContent:
    """
    Scrape article content from a URL.

    Args:
        url: The URL to scrape
        timeout: Request timeout in seconds (default: 10)

    Returns:
        ScrapedContent object with the extracted content or error info
    """
    try:
        # Download the page
        downloaded = trafilatura.fetch_url(url)

        if downloaded is None:
            return ScrapedContent(
                url=url,
                content=None,
                title=None,
                success=False,
                error="Failed to download page",
            )

        # Extract the main content
        content = trafilatura.extract(
            downloaded,
            include_comments=False,
            include_tables=False,
            no_fallback=False,
        )

        # Extract metadata for title
        metadata = trafilatura.extract_metadata(downloaded)
        title = metadata.title if metadata else None

        if content is None or content.strip() == "":
            return ScrapedContent(
                url=url,
                content=None,
                title=title,
                success=False,
                error="No content extracted",
            )

        return ScrapedContent(url=url, content=content, title=title, success=True)

    except Exception as e:
        return ScrapedContent(
            url=url, content=None, title=None, success=False, error=str(e)
        )


def scrape_article_simple(url: str) -> Optional[str]:
    """
    Simple version that just returns the content string or None.

    Args:
        url: The URL to scrape

    Returns:
        The article content as a string, or None if scraping failed
    """
    result = scrape_article(url)
    return result.content if result.success else None


if __name__ == "__main__":
    # Test the scraper
    test_url = "https://www.morgenpost.de/bezirke/treptow-koepenick/article410820425/kurioser-verkehrs-zoff-in-koepenick-weil-behoerde-markierungen-entfernt.html"
    result = scrape_article(test_url)

    if result.success:
        print(f"Title: {result.title}")
        print(f"Content length: {len(result.content)} chars")
        print(f"Preview: {result.content[:500]}...")
        print(f"HTML: {result.content}")
    else:
        print(f"Failed: {result.error}")
