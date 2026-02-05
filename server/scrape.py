import datetime

from serpapi import search

import content_scraper
import myclasses
from db import CRUD
from openrouter import report

# Main execution
database = CRUD.connection("http://pocketbase:8080")
yesterdate = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
date = datetime.datetime.now().strftime("%Y-%m-%d")
query = f"köpenick news after:{yesterdate}"


params = {
    "api_key": "a1f2e133812cbca2dde9173b10d00aed814a914762efb200e568625feccab514",
    "engine": "google",
    "q": query,
    "google_domain": "google.com",
}
print(query)

# 1. Fetch data from Google
searchy = search(params)
results = searchy.as_dict()
savedresponse = results.get("organic_results", [])
print("Found", len(savedresponse), "results")
api_key = "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"

local_articles = []
ids = []
for item in savedresponse:
    print(f"\n--- Checking: {item['title']} ---")

    # Step 1: Quick snippet check (existing)
    is_maybe_local = content_scraper.check_snippet_locality(
        item["snippet"], item["link"], api_key
    )

    if not is_maybe_local:
        print("  ❌ Snippet check: Not local (skipping)")
        continue

    print("  ✓ Snippet check: Possibly local")

    # Step 2: Scrape full article content
    print("  📄 Scraping full content...")
    full_content = content_scraper.scrape_article_simple(item["link"])
    if not full_content:
        print("  ⚠️ Could not scrape content (skipping)")
        continue

    if len(full_content) > 4999:
        print("cutting the scraped content from" + str(len(full_content)) + " to 499")
        full_content = full_content[:4999]

    # Step 3: Deep locality check on full content
    print("  🔍 Deep locality check...")
    is_truly_local = content_scraper.check_full_content_locality(full_content, api_key)

    if not is_truly_local:
        print("  ❌ Deep check: Not truly local (skipping)")
        continue

    print("  ✅ Confirmed local! Saving to database.")

    # Step 4: Save only if truly local
    news = myclasses.News(
        id="",
        type="google",
        source=item["source"],
        title=item["title"],
        description=item["snippet"],
        link=item["link"],
        full_text=full_content,
    )
    # Step 4: Classify badges and save
    badges = database.getbadgefornews(news, api_key)
    # Filter out None values from badge classification
    badges = [badge for badge in badges if badge is not None]
    news.badges = badges
    print(news.tojson(True))
    print("  saving to the database")
    news_id = database.save_news(news)
    ids.append(news_id)
    local_articles.append(news)

print(f"\n{'=' * 50}")
print(
    f"Results: {len(local_articles)} truly local articles from {len(savedresponse)} total"
)

# Only create report and day if we have local articles
if ids:
    report = report.create_and_save_report(database, local_articles)
    day = myclasses.Day(id=date, news=ids, reportid=report.id)
    database.save_day(day)
    print(f"Day saved with {len(ids)} local articles")
else:
    print("No local articles found today - skipping report generation")
