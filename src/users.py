from file_handler import JsonHandler
from display import Display


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
        self.past_searches = set()
        self.city = None

    def save_and_display_data(self, data, flag):
        if flag == "region":
            final_format = {"Region": self.region, "Data": data}
            content = JsonHandler.read_json(self.path)
            content.append(final_format)
            JsonHandler.write_json(self.path, content)
            self.past_searches.add(self.region)
            display_content = Display(final_format)
            display_content.display_saved_data()
        elif flag == "city":
            final_format = {"City": self.city, "Data": data}
            content = JsonHandler.read_json(self.path)
            content.append(final_format)
            JsonHandler.write_json(self.path, content)
            self.past_searches.add(self.city)
            display_content = Display(final_format)
            display_content.display_saved_data()

    def check_past_entries(self, place):
        if place in self.past_searches:
            return True
        elif place not in self.past_searches:
            return False

    def retrieve_saved(self, place):
        content = JsonHandler.read_json(self.path)
        for item in content:
            if "City" in item and item["City"] == list(place):
                return item
            if "Region" in item and item["Region"] == list(place):
                return item

    def search_and_display_data(self, place):
        if self.check_past_entries(place):
            data = self.retrieve_saved(place)
            display_result = Display(data)
            display_result.display_saved_data()
            return True
        else:
            return False

    def history_search(self, place_obj):
        if self.search_and_display_data(self.region):
            return True
        elif not self.search_and_display_data(self.region):
            self.city = place_obj.select_city(self.region)
            if self.search_and_display_data(self.city):
                return True
            else:
                return False
