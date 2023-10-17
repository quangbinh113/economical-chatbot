import datetime


def get_time_format() -> str:
    now = datetime.datetime.utcnow()
    out = f'{now.year}-{now.month}-{now.day}'
    return out