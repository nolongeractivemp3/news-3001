import datetime
import os

from fastapi import FastAPI, HTTPException, Query
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
    try:
        report = connection.get_report_from_day(date)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
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
    try:
        report = db.get_todays_report()
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    print(report)
    return report.text


def _raise_stats_exception(exc: ValueError):
    status_code = 404 if str(exc).startswith("No day found for date:") else 400
    raise HTTPException(status_code=status_code, detail=str(exc)) from exc


@app.get("/stats/day")
def day_stats(date: str = Query(..., description="Date format: YYYY-MM-DD")):
    db = get_database()
    try:
        return db.get_day_stats(date)
    except ValueError as exc:
        _raise_stats_exception(exc)


@app.get("/stats/tags/daily")
def daily_tag_stats(days: int = Query(30, ge=1, le=365)):
    db = get_database()
    try:
        return db.get_tag_usage_by_day(days)
    except ValueError as exc:
        _raise_stats_exception(exc)


@app.get("/stats/summary")
def stats_summary(days: int = Query(30, ge=1, le=365)):
    db = get_database()
    try:
        return db.get_scraper_summary(days)
    except ValueError as exc:
        _raise_stats_exception(exc)


if __name__ == "__main__":
    # run server
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5000)
