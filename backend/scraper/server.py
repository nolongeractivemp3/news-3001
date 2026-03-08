from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .pipeline import run_scraper

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def index():
    return {"service": "scraper", "status": "running"}


@app.post("/run")
def trigger_scraper():
    result = run_scraper()
    return result
