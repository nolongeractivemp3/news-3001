import datetime

from serpapi import search

import myclasses
from content_scraper import scrape_article_simple
from db import CRUD
from openrouter import openrouter_client
from server import get_news


def create_and_save_report(db: CRUD.connection):
    api_key = (
        "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"
    )
    system = """
    You are a News reporter you get some news and you should write a german report about what happend in kopenick.
    Please keep your report short and concise.
    Please respond with simple html only using things like h1, h2, h3 strong p img (img only if you must im not sure it works) with not too long lines.
    only include a short summary of the news.
    shouldent be longer than 1 min to read.
    Keep the language simple and easy to understand but a bit jokey with a touch of humor.
    be a bit left leaning and sarcastic."""
    prompt = ""
    print("found news")
    for data in get_news(database):
        prompt += f"Title: {data.title} Description: {data.description} Source: {data.source} Link: {data.link}\n"
    response = openrouter_client.query_openrouter(
        query=prompt,
        api_key=api_key,
        system_prompt=system,
    )
    report = myclasses.Report(response)
    return db.create_report(report)


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
        model="nex-agi/deepseek-v3.1-nex-n1:free",
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


# Main execution
database = CRUD.connection("http://pocketbase:8080")
yesterdate = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
date = datetime.datetime.now().strftime("%Y-%m-%d")
query = f"köpenick news after:{yesterdate}"

params = {
    "api_key": "a1f2e133812cbca2dde9173b10d00aed814a914762efb200e568625feccab514",
    "engine": "google",
    "q": query,
    "location": "Berlin, Germany",
    "google_domain": "google.de",
    "gl": "de",
    "hl": "de",
    "filter": "0",
}
print(query)

# 1. Fetch data from Google
searchy = search(params)
results = searchy.as_dict()
savedresponse = results.get("organic_results", [])

api_key = "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"

local_articles = []
ids = []

for item in savedresponse:
    print(f"\n--- Checking: {item['title']} ---")

    # Step 1: Quick snippet check (existing)
    is_maybe_local = check_snippet_locality(item["snippet"], item["link"], api_key)

    if not is_maybe_local:
        print(f"  ❌ Snippet check: Not local (skipping)")
        continue

    print(f"  ✓ Snippet check: Possibly local")

    # Step 2: Scrape full article content
    print(f"  📄 Scraping full content...")
    full_content = scrape_article_simple(item["link"])

    if not full_content:
        print(f"  ⚠️ Could not scrape content (skipping)")
        continue

    print(f"  ✓ Scraped {len(full_content)} chars")

    # Step 3: Deep locality check on full content
    print(f"  🔍 Deep locality check...")
    is_truly_local = check_full_content_locality(full_content, api_key)

    if not is_truly_local:
        print(f"  ❌ Deep check: Not truly local (skipping)")
        continue

    print(f"  ✅ Confirmed local! Saving to database.")

    # Step 4: Save only if truly local
    news = myclasses.News(
        source=item["source"],
        title=item["title"],
        description=item["snippet"],
        link=item["link"],
        date=date,
        full_content=full_content,
    )
    news_id = database.save_news(news)
    ids.append(news_id)
    local_articles.append(item)

print(f"\n{'=' * 50}")
print(
    f"Results: {len(local_articles)} truly local articles from {len(savedresponse)} total"
)

# Only create report and day if we have local articles
if ids:
    report_id = create_and_save_report(database)
    print(f"Report created: {report_id}")

    day = myclasses.Day(date=date, NewsIds=ids, Report=report_id)
    database.save_day(day)
    print(f"Day saved with {len(ids)} local articles")
else:
    print("No local articles found today - skipping report generation")
