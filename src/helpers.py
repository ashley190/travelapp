import requests
import json
from file_handler import JsonHandler
from display import Display


class ErrorHandling:
    @classmethod
    def handle_request_errors(cls, func):
        def wrapper(*args, **kwargs):
            func_value = func(*args, **kwargs)
            if func_value[0] >= 500:
                return "Server Error. Try Again"
            elif func_value[0] >= 400:
                return "Request Error. Try Again"
            elif func_value[0] >= 300:
                return "Redirection Error. Try Again"
            return func_value[1]
        return wrapper


class ApiQuery:
    def __init__(self, url, querystring=None, headers=None):
        self.url = url
        self.querystring = querystring
        self.headers = headers

    @ErrorHandling.handle_request_errors
    def get_data(self):
        response = requests.get(
            self.url,
            params=self.querystring,
            headers=self.headers)
        response_code = response.status_code
        data = json.loads(response.text)
        return response_code, data


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

    @classmethod
    def history_search(self, func):
        def wrapper(*args, **kwargs):
            func_value = func(*args, **kwargs)
            return func_value
        return wrapper


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
