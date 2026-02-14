import datetime
import json
import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

import rss
from db import CRUD
from myclasses import News
from openrouter import openrouter_client


def get_database():
    return CRUD.connection(os.getenv("POCKETBASE_URL", "http://pocketbase:8080"))


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


@app.get("/oldnews")
def oldnews(date: str):
    # date format validation
    try:
        datetime.datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format")
    connection = get_database()
    data = connection.get_news_from_day(date)
    response = []
    for news in data:
        response.append(news.tojson(False))
    return response


@app.get("/oldreport")
def oldreport(date: str):
    # date format validation
    try:
        datetime.datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format")
    connection = get_database()
    report = connection.get_report_from_day(date)
    return report.text


@app.get("/")
def index():
    data = get_news()
    json_data = [news.tojson(False) for news in data]
    return json_data


@app.get("/rss")
def rssserver():
    data = rss.get_rss_feed()
    json_data = [news.tojson(False) for news in data]
    return json_data


@app.get("/report")
def report():
    db = get_database()
    report = db.get_todays_report()
    print(report)
    return report.text


if __name__ == "__main__":
    # run server
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5000)
