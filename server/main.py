from db import CRUD
from myclasses import News, Report
from openrouter.report import create_report

if __name__ == "__main__":
    database = CRUD.connection("http://localhost:8080")
    print("Database connection established.")
    create_report(database)
