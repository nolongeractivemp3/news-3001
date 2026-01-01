from db import CRUD
from myclasses import News

if __name__ == "__main__":
    database = CRUD.connection("http://localhost:8080")
    database.get_news_from_day("")
