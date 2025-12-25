import json

import flask_cors
from flask import Flask

from openrouter import openrouter_client

app = Flask(__name__)
flask_cors.CORS(app)


class News:
    def __init__(self, source, title, description, link):
        self.source = source
        self.title = title
        self.description = description
        self.link = link

    def tojson(self):
        return {
            "source": self.source,
            "title": self.title,
            "description": self.description,
            "link": self.link,
        }


def get_news(path) -> list[News]:
    data = []
    raw_datas = open(path, "r").read()
    print(json.loads(raw_datas))
    for raw_data in json.loads(raw_datas):
        title = raw_data["title"]
        description = raw_data["snippet"]
        link = raw_data["link"]
        source = raw_data["source"]
        data.append(News(source, title, description, link))
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
    Please respond with formatted markdown with not too long lines.
    only include a short summary of the news.
    shouldent be longer than 1 min to read.
    Keep the language simple and easy to understand but a bit jokey with a touch of humor.
    be a bit left leaning and sarcastic.
    """
        prompt = ""
        for data in get_news("/app/data/news_data.json"):
            prompt += f"Title: {data.title} Description: {data.description} Source: {data.source} Link: {data.link}\n"
        response = openrouter_client.query_openrouter(
            query=prompt, api_key=api_key, system_prompt=system
        )
        # Cache the new response
        with open(cache_file, "w") as f:
            json.dump(response, f)
        return response


data = get_news("/app/data/news_data.json")
json_data = [news.tojson() for news in data]


@app.route("/")
def index():
    return json_data


@app.route("/report")
def report():
    report = getreport()
    print(report)
    return report


# run server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
