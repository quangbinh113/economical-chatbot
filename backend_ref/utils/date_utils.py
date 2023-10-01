import datetime


def get_time_format() -> str:
    now = datetime.datetime.now()
    #y-m-d
    out = f'{now.year}-{now.month}-{now.day}'
    return out
