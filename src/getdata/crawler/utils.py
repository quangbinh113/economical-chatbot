import time
import json
from datetime import datetime, timedelta
import re
from typing import Union
from src.getdata.crawler.stock_visualizer import StockVisualization

def answer_to_json(answer: str) -> Union[dict, None]:
    """
    Extract json from text
    Args:
        answer(str:None): The text need to extract json from
    Return:
        dict if found the json string else None
    """
    json_regex = r"\{[^{}]*\}"
    json_from_answer = re.findall(json_regex, answer)

    if not json_from_answer:
        return None

    json_from_answer = json_from_answer[0].replace("'", '"')
    res = json.loads(json_from_answer)

    return res


def get_time_range(time_range: str) -> Union[None, timedelta]:
    date_unit = ["ngày", "date", "dates"]
    week_unit = ["tuần", "week", "weeks"]
    month_unit = ["tháng", "months", "month"]
    year_unit = ["year", "years", "năm"]
    try:
        split_time = time_range.split(" ")
        assert len(split_time) == 2

        time_range, time_unit = split_time

        assert time_range.isnumeric()
        time_range = int(time_range)

        if time_unit in date_unit:
            return timedelta(days=time_range)

        if time_unit in week_unit:
            return timedelta(weeks=time_range)

        if time_unit in month_unit:
            return timedelta(days=time_range * 30)

        if time_unit in year_unit:
            return timedelta(days=time_range * 365)

        return None
    except:
        return None


def preprocess_visualize(
    answer: Union[dict,None],
) -> Union[
    dict,
    None
]:
    stock_code = answer["stock_code"]
    time_start = answer["start_date"]
    time_end = answer["end_date"]
    time_range = answer["time_range"]

    validate_time_start = to_datetime(time_start)
    validate_time_end = to_datetime(time_end)

    if stock_code == 'None' or stock_code == None:
        return None

    if not validate_time_start or not validate_time_end:
        return None

    # if not validate_time_start and not validate_time_end:
    #     return None

    if validate_time_end > datetime.today():
        validate_time_end = datetime.today()

    # if 
    #     time_range = get_time_range(time_range)

    return {
        'stock_code':stock_code,
        "start_date": validate_time_start,
        "end_date": validate_time_end,
        "time_range": time_range,
    }


def to_datetime(date_string: str) -> Union[datetime, None]:
    formats = ["%d/%m/%Y %H:%M:%S", "%d/%m/%Y"]
    for format in formats:
        try:
            date_time = datetime.strptime(date_string, format)
            return date_time
        except ValueError:
            pass
    return None


# if __name__ == "__main__":
#     test = 'abcdm {\n  "stock_code": "VHM",\n  "start_date": "11/10/2023 08:00:00",\n  "end_date": "11/10/2023 18:00:00",\n  "time_range": "8 giờ đến 18 giờ"\n}'
#     ans = answer_to_json(test)
#     x = preprocess_visualize(ans)
#     print(x)
#     # print(type(is_valid_datetime("19/10/2023")))
#     plotter = StockVisualization(symbol=x['stock_code'],start_date=x['end_date'],end_date=x['start_date'])

#     plotter.plot_data()