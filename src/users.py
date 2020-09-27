from file_handler import JsonHandler


class User:
    def __init__(self):
        self.name: str = input("What is your name?\n")
        self.path = f"resources/{self.name}_past_searches"

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

    def save_data(self, region, data):
        final_format = {"City": region, "Data": data}
        content = JsonHandler.read_json(self.path)
        content.append(final_format)
        JsonHandler.write_json(self.path, content)

    def check_past_entries(self):
        if self.region in self.past_searches:
            return True
        elif self.region not in self.past_searches:
            self.past_searches.add(self.region)
            return False

    def retrieve_saved(self):
        content = JsonHandler.read_json(self.path)
        for item in content:
            if item["City"] == list(self.region):
                return item
