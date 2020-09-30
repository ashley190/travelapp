import requests
from requests import exceptions
import json
from file_handler import JsonHandler
from display import Display
import sys


class ErrorHandling:
    @classmethod
    def handle_request_errors(cls, response: tuple):
        """Handles request errors resulting from API queries
        with response codes above 299. Application exits if
        response code is more than 299 with an error message
        printed.

        Args:
            response (int): Response output from the get_data method
                of an ApiQuery object.
        """
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
    """Creates ApiQuery object."""

    def __init__(self, url, querystring=None, headers=None):
        """Initialises ApiQuery object with all necessary fields
        to query API endpoint.

        Args:
            url (str): URL/URI to API endpoint
            querystring (dict, optional): Dictionary containing
                required query fields. Defaults to None.
            headers (dict, optional): Dictionary containing required
                header fields. Defaults to None.
        """
        self.url: str = url
        self.querystring: dict = querystring
        self.headers: dict = headers

    def get_data(self) -> tuple:
        """Attempts API query to specified endpoint.

        Tries to query API endpoint using the predefined instance
        attributes and returns required results if successful.
        Application exits if unsuccessful.

        Returns:
            tuple: Tuple containng the response code (int) and
                decoded response data (dict) if successful. \
        """
        try:
            response = requests.get(
                self.url,
                params=self.querystring,
                headers=self.headers)
            response_code: int = response.status_code
            data: dict = json.loads(response.text)
            return response_code, data
        except exceptions.RequestException as error:
            print(error)
            sys.exit("Program exited. Please try again.")


class Helpers:
    """Helper class methods for processing API data."""

    @classmethod
    def key_lookup(cls, target: dict, *keys: str) -> dict:
        """Searches for specific k:v pairs in a target dictionary.

        Searches for specific key, value pairs as defined by the keys
        argument within a target dictionary; extracts and return
        target keys and values.

        Args:
            target (dict): Targetted dictionary for lookup.
            keys (tuple): Variable number of key arguments permitted
                for target lookup.

        Returns:
            dict: Key, value pairs with matching keys as per keys argument.
        """
        key_dict: dict = {}
        for key in keys:
            if key in target:
                key_dict[key] = target[key]
        return key_dict

    @classmethod
    def geo_search(cls, target: dict):
        """Searches for "geos" related data from API query response

        Args:
            target (dict): target dictionary usually resulting from the
            processed response output from the get_data method of an APIQuery
            object querying the locations/autocomplete endpont.

        Returns:
            dict: If successful, result object dictionary from a "geos" type
            result (contains location_id) for poi query.
        """
        for data in target:
            if data["result_type"] == "geos":
                return data["result_object"]

    @classmethod
    def remove_ads(cls, target: list) -> list:
        """Searches and removes ads in target list.

        Args:
            target (list): list of POIs resulting from the get_data() method
                of an APIQuery object querying the attractions/list endpoint
                for points of interest (POIs) - contains embedded ads.

        Returns:
            list: list of POIs with no ads.
        """
        ads_removed: list = []
        for item in target:
            if "ad_position" not in item and "ad_size" not in item:
                ads_removed.append(item)
        return ads_removed


class Decorators:
    @classmethod
    def save_and_display_data(cls, func):
        """Save and display data outputted by inner function.

        Takes the output of the inner function consisting of
        final formatted content and file path; saves and display
        data according to predefined file naming rules and display
        format.

        Args:
            func (func): a function that outputs data and file path
            for saving.
        """
        def wrapper(*args, **kwargs):
            func_value = func(*args, **kwargs)
            content: list = JsonHandler.read_json(func_value[1])
            content.append(func_value[0])
            JsonHandler.write_json(func_value[1], content)
            display_content: Display = Display(content[0])
            display_content.display_saved_data()
            return func_value
        return wrapper
