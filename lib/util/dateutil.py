from datetime import datetime
from datetime import timedelta


def str_to_timestamp(date):
    result = int(datetime.strptime(date, "%a %b %d %H:%M:%S %z %Y").timestamp() * 1000)
    return result


def today_timestamp():
    return int(datetime.now().timestamp() * 1000)


def today_start_day_timestamp():
    s_day = datetime.now().replace(hour=00, minute=00, second=00, microsecond=000000)
    return int(s_day.timestamp() * 1000)


def today_end_day_timestamp():
    e_day = datetime.now().replace(hour=23, minute=59, second=59, microsecond=999999)
    return int(e_day.timestamp() * 1000)


def fifteen_minutes_ago_ts():
    return int((datetime.now() - timedelta(minutes=int(15))).timestamp() * 1000)


def seven_day_timestamp():
    days = datetime.now() - timedelta(days=7)
    return days


def day_end_timestamp(day):
    return (datetime.now() - timedelta(days=int(day)))