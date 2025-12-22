import json

import flask_cors
from flask import Flask

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


data = get_news("/app/data/news_data.json")
json_data = [news.tojson() for news in data]


@app.route("/")
def index():
    return json_data


# run server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
