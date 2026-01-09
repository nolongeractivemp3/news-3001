import datetime
import json

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import rss
from db import CRUD
from myclasses import News
from openrouter import openrouter_client


def get_database():
    return CRUD.connection("http://pocketbase:8080")


database = None

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_news(connection: CRUD.connection | None = None) -> list[News]:
    if connection is None:
        connection = get_database()
    data = connection.get_news_from_day(datetime.datetime.now().strftime("%Y-%m-%d"))
    return data


@app.get("/")
def index():
    data = get_news()
    json_data = [news.tojson() for news in data]
    return json_data


@app.get("/rss")
def rssserver():
    data = rss.get_rss_feed()
    json_data = [news.tojson() for news in data]
    return json_data


@app.get("/report")
def report():
    db = get_database()
    report = db.get_todays_report()
    print(report)
    return report.Summary


@app.get("/badges")
def badges():
    db = get_database()
    all_badges = db.getallbadges()
    return [badge.todict() for badge in all_badges]


if __name__ == "__main__":
    # run server
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5000)
