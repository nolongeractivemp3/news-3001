import json

from serpapi import search

query = "köpenick news after:2025-12-20"
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

organic_results = results.get("organic_results", [])
with open("./data/news_data.json", "w", encoding="utf-8") as f:
    json.dump(organic_results, f, indent=4, ensure_ascii=False)

print(f"Successfully saved {len(organic_results)} articles.")
