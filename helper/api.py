from pydantic import BaseModel
from typing import Optional
import requests


class AIResponseModel(BaseModel):
    cau_tra_loi: Optional[str]


def get_data_from_api(api_url, data: {}) -> AIResponseModel:
    try:
        # print(data)
        # Send a GET request to the API endpoint
        response = requests.post(api_url, json=data)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response into your Pydantic model
            api_data = response.json()
            data_model = AIResponseModel(**api_data)
            return data_model
        else: 
            # Handle non-200 status codes if needed
            raise Exception("invalid data")  # Or raise an exception

    except requests.exceptions.RequestException as e:
        # Handle request exceptions
        print(f"Request Error: {str(e)}")
        raise Exception("invalid data")  # Or raise an exc

# def streaming_response(api_url,data):
#     try:
#         response = requests.post(api_url,json=data,stream = True)
#     except:
#         pass