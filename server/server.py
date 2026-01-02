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


def get_news() -> list[News]:
    data = database.get_news_from_day(datetime.datetime.now().strftime("%Y-%m-%d"))
    data = data + rss.get_rss_feed()

    return data


def getreport():
    # Cache the response to avoid repeated API calls for the same data
    cache_file = "/app/data/chache/report_cache.json"
    try:
        with open(cache_file, "r") as f:
            cached_response = json.load(f)
        return cached_response
    except (FileNotFoundError, json.JSONDecodeError):
        api_key = (
            "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"
        )
        system = """
    You are a News reporter you get some news and you should write a german report about what happend in kopenick.
    Please keep your report short and concise.
    Please respond with simple html only using things like h1, h2, h3 strong p img (img only if you must im not sure it works) with not too long lines.
    only include a short summary of the news.
    shouldent be longer than 1 min to read.
    Keep the language simple and easy to understand but a bit jokey with a touch of humor.
    be a bit left leaning and sarcastic.
    """
        prompt = ""
        for data in get_news():
            prompt += f"Title: {data.title} Description: {data.description} Source: {data.source} Link: {data.link}\n"
        response = openrouter_client.query_openrouter(
            query=prompt,
            api_key=api_key,
            system_prompt=system,
            model="nex-agi/deepseek-v3.1-nex-n1:free",
        )
        # Cache the new response
        with open(cache_file, "w") as f:
            json.dump(response, f)
        return response


@app.route("/")
def index():
    data = get_news()
    json_data = [news.tojson() for news in data]
    return json_data


@app.route("/report")
def report():
    report = getreport()
    print(report)
    return report


if __name__ == "__main__":
    # run server
    app.run(host="0.0.0.0", port=5000)
