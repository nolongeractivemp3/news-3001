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
