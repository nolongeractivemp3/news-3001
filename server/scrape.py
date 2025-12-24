import datetime
import json
import os

from serpapi import search

from openrouter import openrouter_client

day = int(datetime.datetime.now().strftime("%d")) - 1
date = datetime.datetime.now().strftime("%Y-%m-") + str(day)
query = f"köpenick news after:{date}"
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
path = "/news3001/data/news_data.json"
# local
# path = "../data/news_data.json"
organic_results = results.get("organic_results", [])
with open(path, "w", encoding="utf-8") as f:
    json.dump(organic_results, f, indent=4, ensure_ascii=False)
savedresponse = open(path, "r", encoding="utf-8")
data = json.load(savedresponse)
api_key = "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"
querry = """You are a News expert.
Following is the description and link of the website.
Please respond with Dumb if
1. the website is not about Köpenick or the wider area like Treptow around it.
Please respond with Smart if
2. the website is about Köpenick or the wider area like Treptow around it.
"""
nicedata = []
for item in data:
    # print(f"Description: {item['snippet']} Link: {item['link']}")
    response = openrouter_client.query_openrouter(
        f"Description: {item['snippet']} Link: {item['link']}",
        api_key,
        system_prompt=querry,
    )
    if response == "Smart":
        nicedata.append(item)


with open(path, "w", encoding="utf-8") as f:
    json.dump(nicedata, f, indent=4, ensure_ascii=False)

# print(f"Successfully saved {len(organic_results)} articles.")

os.system("rm -rf /news3001/data/chache/report_cache.json")
