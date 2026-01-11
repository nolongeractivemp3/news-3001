from datetime import datetime

from typing_extensions import List


class Badge:
    def __init__(self, name: str, description: str, id: str, color: str):
        """Initialize a badge object.

        Args:
            name (str): The name of the badge.
            description (str): The description of the badge.
            id (str): The unique identifier of the badge.
            color (str): The color of the badge.
        """
        self.id: str = id
        self.name: str = name
        self.description: str = description
        self.color: str = color

    def todict(self):
        return {
            "Id": self.id,
            "Name": self.name,
            "Description": self.description,
            "Color": self.color,
        }


class News:
    def __init__(
        self,
        id: str,
        type: str,
        title: str,
        description: str,
        full_text: str,
        source: str,
        link: str,
        badges: List[Badge] = [],
    ):
        """Initialize a News object.

        Args:
            id (str): The unique identifier of the news item.
            type (str): The type of the news item.
            title (str): The title of the news item.
            description (str): The description of the news item.
            full_text (str): The full text of the news item.
            source (str): The source of the news item.
            link (str): The link to the news item.
            badges (List[Badge]): The badges associated with the news item.
        """
        self.id = id
        self.type = type
        self.title = title
        self.description = description
        self.full_text = full_text
        self.source = source
        self.link = link
        self.badges = badges

    def tojson(self, badgeid: bool):
        returndict = {
            "id": self.id,
            "type": self.type,
            "title": self.title,
            "description": self.description,
            "full_text": self.full_text,
            "source": self.source,
            "link": self.link,
            "badges": [badge.todict() for badge in self.badges],
        }
        if badgeid:
            returndict["badges"] = [badge.id for badge in self.badges]
        return returndict


class Report:
    def __init__(
        self,
        id: str = datetime.now().strftime("%Y-%m-%d"),
        text: str = "somethings fucked",
    ):
        self.id: str = id
        self.text: str = text

    def tojson(self):
        return {
            "id": self.id,
            "text": self.text,
        }


class Day:
    def __init__(self, id, news, reportid):
        self.id = id
        self.news = news
        self.reportid = reportid

    def tojson(self):
        return {
            "id": self.id,
            "news": self.news,
            "report": self.reportid,
        }
