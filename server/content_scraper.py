"""
Content Scraper Module

A reusable module for extracting article content from URLs.
Can be used for news articles, blog posts, or any web content.
"""

from dataclasses import dataclass
from typing import Optional

import trafilatura

from openrouter import openrouter_client


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


def check_snippet_locality(snippet: str, link: str, api_key: str) -> bool:
    """
    Quick check: Is the snippet about Köpenick? (existing check)
    Returns True if "Smart", False if "Dumb"
    """
    system_prompt = """You are a News expert.
Following is the description and link of the website.
Please respond with Dumb if
1. the website is not about Köpenick or the wider area like Treptow around it.
Please respond with Smart if
2. the website is about Köpenick or the wider area like Treptow around it.
"""
    response = openrouter_client.query_openrouter(
        f"Description: {snippet} Link: {link}",
        model="tngtech/deepseek-r1t2-chimera:free",
        api_key=api_key,
        system_prompt=system_prompt,
    )
    return response.strip() == "Smart"


def check_full_content_locality(content: str, api_key: str) -> bool:
    """
    Deep check: Is the full article actually about Köpenick?
    Returns True if local, False if not local
    """
    system_prompt = """You are a local news expert for Berlin-Köpenick.
You will receive the full text of a news article.
Your task is to determine if this article is TRULY LOCAL to Köpenick or the surrounding area (Treptow-Köpenick, Friedrichshagen, Müggelheim, Grünau, etc.)

Respond with ONLY one word:
- "Local" if the article is specifically about Köpenick or its surrounding areas
- "NotLocal" if the article only mentions Köpenick in passing, or is about broader Berlin/Germany/World news
- also respond with NotLocal if its not the full atrical like if its behind a paywall


Be strict: The article must be PRIMARILY about something happening IN Köpenick, not just mentioning it."""

    # Truncate content if too long (keep first 4000 chars to stay within token limits)
    truncated_content = content[:4000] if len(content) > 4000 else content

    response = openrouter_client.query_openrouter(
        f"Article content:\n{truncated_content}",
        api_key,
        system_prompt=system_prompt,
    )
    return response.strip() == "Local"
