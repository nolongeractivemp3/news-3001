import datetime
import json

from serpapi import search

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

# 1. Fetch data
searchy = search(params)
results = searchy.as_dict()
# path = "/news3001/data/news_data.json"
# local
path = "../data/news_data.json"
organic_results = results.get("organic_results", [])
with open(path, "w", encoding="utf-8") as f:
    json.dump(organic_results, f, indent=4, ensure_ascii=False)

print(f"Successfully saved {len(organic_results)} articles.")
