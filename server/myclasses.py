from typing_extensions import List


class Badge:
    def __init__(self, name: str, description: str, id: str):
        """Initialize a badge object.

        Args:
            name (str): The name of the badge.
            description (str): The description of the badge.
            id (str): The unique identifier of the badge.
        """
        self.id: str = id
        self.name: str = name
        self.description: str = description

    def todict(self):
        return {
            "Id": self.id,
            "Name": self.name,
            "Description": self.description,
        }


class News:
    def __init__(
        self,
        source,
        title,
        description,
        link,
        date,
        full_content=None,
        badges: List[Badge] = [],
    ):
        self.source = source
        self.title = title
        self.description = description
        self.link = link
        self.date = date
        self.full_content = full_content
        self.badges = badges

    def tojson(self):
        returndict = {
            "Source": self.source,
            "Title": self.title,
            "description": self.description,
            "link": self.link,
            "date": self.date,
            "full_content": self.full_content,
        }
        if self.badges:
            returndict["badges"] = [badge.todict() for badge in self.badges]
        return returndict


class Report:
    def __init__(self, Summary: str):
        self.Summary: str = Summary


class Day:
    def __init__(self, date, NewsIds, Report: str):
        self.date = date
        self.NewsIds = NewsIds
        self.Report: str = Report

    def tojson(self):
        return {
            "date": self.date,
            "News": self.NewsIds,
            "Report": self.Report,
        }

    def todict(self):
        return {
            "date": self.date,
            "News": self.NewsIds,
            "Report": self.Report,
        }
