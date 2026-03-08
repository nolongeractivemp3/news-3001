import myclasses
from openrouter.badges import get_badges


def get_badge_by_id(client, badge_id: str) -> myclasses.Badge:
    raw_badge = client.collection("badges").get_one(badge_id)
    return myclasses.Badge(
        raw_badge.name,
        raw_badge.description,
        raw_badge.id,
        raw_badge.hexcolor,
    )


def get_all_badges(client) -> list[myclasses.Badge]:
    badges: list[myclasses.Badge] = []
    for badge in client.collection("badges").get_full_list():
        badges.append(
            myclasses.Badge(
                badge.name,
                badge.description,
                badge.id,
                badge.hexcolor,
            )
        )
    return badges


def get_badges_for_news(client, news: myclasses.News, key: str):
    return get_badges(news, get_all_badges(client), key)
