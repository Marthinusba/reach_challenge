import requests
import json
from time import sleep
from random import randint

class ApiData:
    """
    A class to represent API data.

    ...

    Attributes
    ----------
    api_response : json object
        The API response.

    Methods
    -------
    read_json():
        Parse JSON object to dictionary.
    """
    def __init__(self, api_response):
        self.api_response = api_response

    def read_json(self):
        """
        Parse JSON object to dictionary.

        Returns
        -------
        json_data : dict
            Parsed JSON data.
        """
        json_data = json.loads(self)
        return json_data


def call_api(api_url):
    """
    Call API.

    Call and return API information and ensure the API is treated kindly.

    Parameters
    ----------
    api_url : str
        The URL of the API.

    Returns
    -------
    data : json object
        JSON object returned by the API.
    """
    try:
        data = requests.get(api_url, timeout=10).json()
    except requests.Timeout:
        # Retry on timeout
        for _ in range(3):
            sleep(randint(10, 1000))
            try:
                data = requests.get(api_url, timeout=10).json()
                break
            except requests.Timeout:
                print("Timed out error received")
    except requests.TooManyRedirects:
        print("URL location is bad")
    except requests.RequestException as e:
        print(f"Request Exception: {e}")
        raise SystemExit(e)

    return json.dumps(data)
