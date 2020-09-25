class User:
    def __init__(self):
        self.name: str = input("What is your name?\n")

    def set_API_key(self, file_path=".env"):
        print("""
        You can obtain an API key when you Sign up and subscribe to the Tripadvisor API on RapidAPI.
        URL: https://rapidapi.com/apidojo/api/tripadvisor1""")
        user_key = input("Please enter your API key here\n")
        with open(file_path, "w") as file:
            file.write(f"API_KEY={user_key}")
            print("API key saved as a persistent environment variable")
