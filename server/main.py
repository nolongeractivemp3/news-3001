import os
from datetime import datetime

from db import CRUD
from myclasses import Badge, News, Report
from openrouter.badges import get_badges
from scraper.storage import save_day_report
from server import get_news

if __name__ == "__main__":
    db = CRUD.connection(os.getenv("POCKETBASE_URL", "http://localhost:8080"))
    article = News(
        title="Test Article",
        id="id1",
        type="google",
        description="Test description",
        full_text="file1",
        source="source1",
        link="https://example.com",
    )
    save_day_report([article], ["myaewj29oxk8qvc"], db)
    response = "<p><strong>Hinweis: Diese Zusammenfassung wurde automatisch mit KI erstellt und nicht auf faktische Richtigkeit überprüft.</strong></p>"
