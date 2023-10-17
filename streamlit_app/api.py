from pydantic import BaseModel
from typing import Optional
import requests
from schemas import AIResponseModel


def get_data_from_api(api_url, data: {}) -> AIResponseModel:
    # try:
    # print(data)
    # Send a GET request to the API endpoint
    print('api_url: ', api_url)
    response = requests.post(api_url, json=data)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response into your Pydantic model
        api_data = response.json()
        print(api_data)
        data_model = AIResponseModel(**api_data)
        return data_model
        # else:
        #     # Handle non-200 status codes if needed
        #     raise Exception("invalid data")  # Or raise an exception

    # except requests.exceptions.RequestException as e:
    #     # Handle request exceptions
    #     print(f"Request Error: {str(e)}")
    #     raise Exception("invalid data")  # Or raise an exc


def save_data_to_db(question, full_response, path_html):
    api_url = "http://127.0.0.1:8000/ai/history/automaticQA"  # Update with your API URL
    data = {
        "question": question,
        "answer": {
            "Content": full_response,
            "Metadata": {"location": path_html}
        }
    }

    response = requests.post(api_url, json=data)

    if response.status_code == 200:
        print("Data saved to the database successfully.")
    else:
        print(f"Error saving data to the database: {response.status_code}")


def upload_file_to_api(UPLOAD_API_URL, file):
    try:
        response = requests.post(UPLOAD_API_URL, files={"file": file})
        if response.status_code == 200:
            return response.json()
        else:
            # st.sidebar.error(f"Failed to upload file: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        # st.sidebar.error(f"Failed to upload file: {str(e)}")
        return None


def read_file(url: str):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            # st.sidebar.error(f"Failed to upload file: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        # st.sidebar.error(f"Failed to upload file: {str(e)}")
        return None


def create_thread(url: str):
    try:
        response = requests.post(url)
        if response.status_code == 200:
            return response.json()
        else:
            # st.sidebar.error(f"Failed to upload file: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        # st.sidebar.error(f"Failed to upload file: {str(e)}")
        return None


def check_thread(url: str):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            # st.sidebar.error(f"Failed to upload file: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        # st.sidebar.error(f"Failed to upload file: {str(e)}")
        return None
