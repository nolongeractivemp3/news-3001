import datetime

from serpapi import search

import myclasses
from db import CRUD
from openrouter import openrouter_client, report

database = CRUD.connection("http://localhost:8080")
yesterdate = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
date = datetime.datetime.now().strftime("%Y-%m-%d")
query = f"köpenick news after:{yesterdate}"
params = {
    "api_key": "a1f2e133812cbca2dde9173b10d00aed814a914762efb200e568625feccab514",
    "engine": "google",
    "q": query,
    "location": "Berlin, Germany",
    "google_domain": "google.de",
    "gl": "de",  # German region
    "hl": "de",  # German language
    "filter": "0",
}
print(query)
# 1. Fetch data
searchy = search(params)
results = searchy.as_dict()
savedresponse = results.get("organic_results", [])

api_key = "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"
querry = """You are a News expert.
Following is the description and link of the website.
Please respond with Dumb if
1. the website is not about Köpenick or the wider area like Treptow around it.
Please respond with Smart if
2. the website is about Köpenick or the wider area like Treptow around it.
"""
nicedata = []
ids = []
for item in savedresponse:
    # print(f"Description: {item['snippet']} Link: {item['link']}")
    response = openrouter_client.query_openrouter(
        f"Description: {item['snippet']} Link: {item['link']}",
        api_key,
        system_prompt=querry,
    )
    if response == "Smart":
        nicedata.append(item)

    news = myclasses.News(
        source=item["source"],
        title=item["title"],
        description=item["snippet"],
        link=item["link"],
        date=date,
    )
    ids.append(database.save_news(news))

report_id = report.create_and_save_report(database)
print(report_id)
news = myclasses.Day(date=date, NewsIds=ids, Report=report_id)

database.save_day(news)

# Generate and save the report

print(
    f"Successfully saved {len(nicedata)} articles from {len(savedresponse)} total results."
)
