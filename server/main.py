from datetime import datetime
import os

from db import CRUD
from myclasses import Badge, News, Report
from openrouter.badges import get_badges
from server import get_news

if __name__ == "__main__":
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("Missing OPENROUTER_API_KEY environment variable.")
    url = os.getenv("POCKETBASE_URL", "http://localhost:8080")
    database = CRUD.connection(url)
    print("Database connection established.")
    news = database.get_news_from_id("5nf3e4lxchz2dmk")
    news.id = ""
    news.badges = database.getbadgefornews(news, api_key)
    print(news.tojson(False))
    database.save_news(news)
