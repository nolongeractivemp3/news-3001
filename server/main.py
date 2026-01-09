from datetime import datetime

from db import CRUD
from myclasses import Badge, News, Report
from openrouter.badges import get_badges
from server import get_news

if __name__ == "__main__":
    url = "http://localhost:8080"
    database = CRUD.connection(url)
    print("Database connection established.")
    example_news = News(
        title="Example Title",
        full_content="Example Content",
        description="Example Description",
        source="Example Source",
        link="https://example.com",
        date=str(datetime.now()),
        badges=[Badge("Example Badge", "https://example.com/badge", "zeitung")],
    )
    database.save_news(example_news)
