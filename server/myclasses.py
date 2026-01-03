class News:
    def __init__(self, source, title, description, link, date, full_content=None):
        self.source = source
        self.title = title
        self.description = description
        self.link = link
        self.date = date
        self.full_content = full_content

    def tojson(self):
        return {
            "source": self.source,
            "title": self.title,
            "description": self.description,
            "link": self.link,
            "date": self.date,
            "full_content": self.full_content,
        }

    def todict(self):
        return {
            "Source": self.source,
            "Title": self.title,
            "description": self.description,
            "link": self.link,
            "date": self.date,
            "full_content": self.full_content,
        }


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
