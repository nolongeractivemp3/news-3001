from myclasses import Badge, News
from openrouter.openrouter_client import query_openrouter


def get_badges(news: News, badges: list[Badge], key: str):
    systemprompt = """You are a helpful newsassistant that is given a list of News and some information about them
    your task to is to find all topics that fit the news. the user will give you a a news artical and a list of topics and your
   goal is to find the best topics for the news article. return the topics in this format topic1id,topic2id,topic3id """
    prompt = f"""#News
    {news.tojson()}
    # badges
    """
    for badge in badges:
        prompt += f"\n{badge.todict()}"
    response = query_openrouter(prompt, key, system_prompt=systemprompt)
    rawtags = response.split(",")
    tags = []
    for tag in rawtags:
        tags.append(next((tagreal for tagreal in badges if tagreal.id == tag), None))
    print(tags)
    return tags
