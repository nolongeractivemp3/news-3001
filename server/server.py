import json

import flask_cors
from flask import Flask

app = Flask(__name__)
flask_cors.CORS(app)


@app.route("/")
def index():
    data = []

    raw_datas = open("/app/data/news_data.json", "r").read()
    print(json.loads(raw_datas))
    for raw_data in json.loads(raw_datas):
        title = raw_data["title"]
        description = raw_data["snippet"]
        link = raw_data["link"]
        source = raw_data["source"]
        data.append(
            {"source": source, "title": title, "description": description, "link": link}
        )
    return data


# run server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
