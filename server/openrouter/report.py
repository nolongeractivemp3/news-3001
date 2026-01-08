import openrouter.openrouter_client
from db import CRUD
from myclasses import News, Report


def create_and_save_report(db: CRUD.connection, news: list[News]):
    api_key = (
        "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"
    )
    system = """
    You are a News reporter you get some news and you should write a german report about what happend in kopenick.
    Please keep your report short and concise.
    Please respond with simple html only using things like h1, h2, h3 strong p img (img only if you must im not sure it works) with not too long lines.
    only include a short summary of the news.
    shouldent be longer than 1 min to read.
    important: please dont include extra empty lines
    Keep the language simple and easy to understand but a bit jokey with a touch of humor.
    be a bit left leaning and sarcastic."""
    prompt = ""
    print("found news")
    for data in news:
        prompt += f"Title: {data.title} Description: {data.description} Source: {data.source} Link: {data.link}\n"
    response = openrouter.openrouter_client.query_openrouter(
        query=prompt,
        api_key=api_key,
        system_prompt=system,
        model="xiaomi/mimo-v2-flash:free",
    )
    report = Report(response)
    return db.create_report(report)
