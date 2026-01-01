class News:
    def __init__(self, source, title, description, link, date):
        self.source = source
        self.title = title
        self.description = description
        self.link = link
        self.date = date

    def tojson(self):
        return {
            "source": self.source,
            "title": self.title,
            "description": self.description,
            "link": self.link,
            "date": self.date,
        }

    def todict(self):
        return {
            "Source": self.source,
            "Title": self.title,
            "description": self.description,
            "link": self.link,
            "date": self.date,
        }


class Day:
    def __init__(self, date, NewsIds):
        self.date = date
        self.NewsIds = NewsIds

    def tojson(self):
        return {
            "date": self.date,
            "News": self.NewsIds,
        }

    def todict(self):
        return {
            "date": self.date,
            "News": self.NewsIds,
        }
