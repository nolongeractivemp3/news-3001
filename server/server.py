import datetime
import json

import flask_cors
from flask import Flask

import rss
from db import CRUD
from myclasses import News
from openrouter import openrouter_client

database = CRUD.connection("http://pocketbase:8080")

app = Flask(__name__)
flask_cors.CORS(app)


def get_news(connection: CRUD.connection) -> list[News]:
    data = connection.get_news_from_day(datetime.datetime.now().strftime("%Y-%m-%d"))
    return data


@app.route("/")
def index():
    data = get_news(database)
    json_data = [news.tojson() for news in data]
    return json_data


@app.route("/rss")
def rssserver():
    data = rss.get_rss_feed()
    json_data = [news.tojson() for news in data]
    return json_data


@app.route("/report")
def report():
    report = database.get_todays_report()
    print(report)
    return report.Summary


if __name__ == "__main__":
    # run server
    app.run(host="0.0.0.0", port=5000)
