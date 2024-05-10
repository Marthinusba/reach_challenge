
import requests
import json
from time import sleep
from random import randint

class apiData():
    def __init__(self,api_response):
        self.api_response = api_response
    def read_json(self):
        json_data = json.loads(self)
        return json_data

def call_api(api_url):
    """
    Call api

    Call and return api information and ensure api is treated kindly

    Parameters
    ----------
    None
    Returns
    -------
    data: json object
        json object returned by api

    """
    #if error dont pull in data
    try:
        data = requests.get(api_url,timeout=10).json()
    #timeout exception
    except requests.Timeout:
        try:
            for _ in range(3):
                sleep(randint(10,1000))
                data = requests.get(api_url,timeout=10).json()
        except:
            print("Timed out error recieved")
    #redirect exception
    except requests.TooManyRedirects:
        print("URL location is bad")
    #request exception
    except requests.RequestException as e:
        raise SystemExit(e)
    return json.dumps(data)



