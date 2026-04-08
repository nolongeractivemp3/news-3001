from myclasses import Badge, News
from openrouter.openrouter_client import query_openrouter


def get_badges(news: News, badges: list[Badge], key: str):
    systemprompt = """You are a classification specialist.
    Your task is to identify matching topics for news articles.
    STRICT RULES:
    1. ONLY return the topic IDs.
    2. Separate multiple IDs with a comma (e.g., id1,id2).
    3. If no topics match, return "keine".
    4. NEVER include explanations, reasoning, or markdown (no bolding, no bullets).
    5. DO NOT mention topics that do not apply."""
    prompt = f"""# News
    {news.tojson(True)}\n# badges"""
    for badge in badges:
        prompt += f"\n{badge.todict()}"
    response = query_openrouter(prompt, key, system_prompt=systemprompt)
    rawtags = response.split(",")
    tags = []
    for tag in rawtags:
        tags.append(next((tagreal for tagreal in badges if tagreal.id == tag), None))
    print(tags)
    return tags
