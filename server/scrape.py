import datetime

from serpapi import search

import myclasses
from db import CRUD
from openrouter import openrouter_client
from server import get_news


def create_and_save_report(db: CRUD.connection):
    # Cache the response to avoid repeated API calls for the same data
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
    # Cache the new response
    #


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

report_id = create_and_save_report(database)

print(report_id)
news = myclasses.Day(date=date, NewsIds=ids, Report=report_id)

database.save_day(news)

# Generate and save the report

print(
    f"Successfully saved {len(nicedata)} articles from {len(savedresponse)} total results."
)
