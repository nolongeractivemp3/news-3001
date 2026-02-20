import datetime

import myclasses


def create_report(client, report: myclasses.Report) -> str:
    print(f"Saving report id:{report.id}")
    return client.collection("report").create(report.tojson()).id


def get_report_from_day(client, date: str) -> myclasses.Report:
    raw_days = client.collection("Days").get_full_list(
        query_params={"filter": f"id = '{date}'"}
    )
    if len(raw_days) == 0:
        raise ValueError(f"No day found for date: {date}")
    report_id = raw_days[0].report
    if not report_id:
        raise ValueError(f"No report linked for date: {date}")
    report = client.collection("Report").get_one(report_id)
    return myclasses.Report(report.id, report.text)


def get_todays_report(client) -> myclasses.Report:
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    return get_report_from_day(client, today)
