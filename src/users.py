from file_handler import JsonHandler
from display import Display
from helpers import Helpers, Decorators


class User:
    def __init__(self):
        self.name: str = input("What is your name?\n")
        self.path = f"resources/{self.name}-saved.json"

    def set_API_key(self, file_path=".env"):
        print("""
        You can obtain an API key when you sign up
        and subscribe to the Tripadvisor API on RapidAPI.
        URL: https://rapidapi.com/apidojo/api/tripadvisor1""")
        user_key = input("Please enter your API key here\n")
        with open(file_path, "w") as file:
            file.write(f"API_KEY={user_key}")
            print("API key saved as a persistent environment variable")

    def API_key_check(self, file_path=".env"):
        try:
            with open(file_path, "r") as file:
                content = file.read()
                if "API_KEY" in content:
                    return True
        except FileNotFoundError:
            return False


class UserFile:
    def __init__(self, region, path):
        self.path = path
        self.region = region
        self.city = None
        self.past_searches = JsonHandler.read_json(
            f"{self.path}search_history")

    @Decorators.save_and_display_data
    def read_flag_and_save(self, data, flag):
        if flag == "region":
            final_format = {"Region": self.region, "Data": data}
            file_path = f"{self.path}{self.region[0]}-{self.region[1]}"
            self.past_searches.append(self.region)
            JsonHandler.write_json(
                f"{self.path}search_history", self.past_searches)
        elif flag == "city":
            final_format = {"City": self.city, "Data": data}
            file_path = f"{self.path}{self.city[0]}-{self.city[1]}"
            self.past_searches.append(self.city)
            JsonHandler.write_json(
                f"{self.path}search_history", self.past_searches)
        return final_format, file_path

    def retrieve_saved(self, place, file_path):
        content = JsonHandler.read_json(file_path)
        for item in content:
            if "City" in item and item["City"] == place:
                return item
            if "Region" in item and item["Region"] == place:
                return item

    @Helpers.history_search
    def search_and_display_data(self, place, file_name):
        path = f"{self.path}{file_name}"
        if place in self.past_searches:
            data = self.retrieve_saved(place, path)
            display_result = Display(data)
            display_result.display_saved_data()
            return True
        else:
            return False
