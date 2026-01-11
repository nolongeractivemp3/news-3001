from datetime import datetime

from db import CRUD
from myclasses import Badge, News, Report
from openrouter.badges import get_badges
from server import get_news

if __name__ == "__main__":
    api_key = (
        "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"
    )
    url = "http://localhost:8080"
    database = CRUD.connection(url)
    print("Database connection established.")
    news = database.get_news_from_id("5nf3e4lxchz2dmk")
    news.id = ""
    news.badges = database.getbadgefornews(news, api_key)
    print(news.tojson())
    database.save_news(news)
