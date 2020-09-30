import requests
from requests import exceptions
import json
from file_handler import JsonHandler
from display import Display
import sys


class ErrorHandling:
    @classmethod
    def handle_request_errors(cls, response):
        error = False
        if response[0] >= 500:
            print(f"Server Error. Message: {response[1]}")
            error = True
        elif response[0] >= 400:
            print(f"Request Error. Message: {response[1]}")
            error = True
        elif response[0] >= 300:
            print(f"Redirection Error. Message: {response[1]}")
            error = True
        if error:
            sys.exit("Program exited. Please try again.")


class ApiQuery:
    def __init__(self, url, querystring=None, headers=None):
        self.url = url
        self.querystring = querystring
        self.headers = headers

    def get_data(self):
        try:
            response = requests.get(
                self.url,
                params=self.querystring,
                headers=self.headers)
            response_code = response.status_code
            data = json.loads(response.text)
            return response_code, data
        except exceptions.RequestException as error:
            print(error)
            sys.exit("Program exited. Please try again.")


class Helpers:
    @classmethod
    def key_lookup(cls, target, *keys):
        key_dict = {}
        for key in keys:
            if key in target:
                key_dict[key] = target[key]
        return key_dict

    @classmethod
    def geo_search(cls, target):
        for data in target:
            if data["result_type"] == "geos":
                return data["result_object"]

    @classmethod
    def remove_ads(cls, target):
        ads_removed = []
        for item in target:
            if "ad_position" not in item and "ad_size" not in item:
                ads_removed.append(item)
        return ads_removed


class Decorators:
    @classmethod
    def save_and_display_data(cls, func):
        def wrapper(*args, **kwargs):
            func_value = func(*args, **kwargs)
            content = JsonHandler.read_json(func_value[1])
            content.append(func_value[0])
            JsonHandler.write_json(func_value[1], content)
            display_content = Display(content[0])
            display_content.display_saved_data()
            return func_value
        return wrapper
