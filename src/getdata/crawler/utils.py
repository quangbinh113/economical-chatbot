import time
import json
from datetime import datetime,timedelta
import re
from typing import Union
def answer_to_json(answer: str)->Union[dict,None]:
    '''
        Extract json from text 
        Args: 
            answer(str:None): The text need to extract json from
        Return:
            dict if found the json string else None
    '''
    json_regex = r'\{[^{}]*\}'
    json_from_answer = re.findall(json_regex,answer)

    if not json_from_answer:
        return None
    
    json_from_answer = json_from_answer[0].replace("'",'"')
    res = json.loads(json_from_answer)

    return res 

def get_time_range(time_range:str) -> Union[None,timedelta]:
    date_unit = ['ngày', 'date', 'dates']
    week_unit = ['tuần','week','weeks']
    month_unit = ['tháng','months','month']
    year_unit = ['year','years','năm']
    try:
        split_time = time_range.split(' ')
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
            return timedelta(days=time_range *365)

        return None    
    except:
        return None
    
def preprocess_visualize(answer:dict)->Union[tuple[Union[None,str],Union[None,str],Union[None,str]],None]:
    time_start = answer['time_start']
    time_end = answer['time_end']
    time_range = answer['time_range']

    # try: 
    # except:




if __name__ == '__main__':
    test = 'abcdm {\n  "stock_code": "VHM",\n  "start_date": "11/10/2023 08:00:00",\n  "end_date": "11/10/2023 18:00:00",\n  "time_range": "8 giờ đến 18 giờ"\n}'
    print((answer_to_json(test)))
    