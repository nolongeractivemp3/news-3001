import datetime
import json

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import rss
from db import CRUD
from myclasses import News
from openrouter import openrouter_client

database = CRUD.connection("http://pocketbase:8080")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_news(connection: CRUD.connection) -> list[News]:
    data = connection.get_news_from_day(datetime.datetime.now().strftime("%Y-%m-%d"))
    return data


@app.get("/")
def index():
    data = get_news(database)
    json_data = [news.tojson() for news in data]
    return json_data


@app.get("/rss")
def rssserver():
    data = rss.get_rss_feed()
    json_data = [news.tojson() for news in data]
    return json_data


@app.get("/report")
def report():
    report = database.get_todays_report()
    print(report)
    return report.Summary


if __name__ == "__main__":
    # run server
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5000)
