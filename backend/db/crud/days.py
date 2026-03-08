import myclasses


def save_day(client, day: myclasses.Day) -> str:
    return client.collection("days").create(day.tojson()).id
