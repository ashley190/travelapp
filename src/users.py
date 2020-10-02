import os
import sys


class User:
    """Generates user object."""

    def __init__(self, test: bool = False):
        """Initialises user object by checking API_key existence.

        If key does not exist, user will be prompted to enter API key.
        This is then saved and application will be rebooted that will
        then be able to detect and access the API key before proceeding
        with the next step of the application.

        Args:
            test (bool) = For testing purposes, no process happens under
                test conditions to allow for manual input of test conditions.
                Defaults to False.
        """
        if not test:
            while not self.API_key_check():
                self.set_API_key()
            self.set_attributes()

    def set_attributes(self):
        """Sets User object attributes.

        Takes in user input to generate instance attributes.
        """
        #: str: store user input into self.name attribute
        self.name: str = input("What is your name?\n")

        #: str: defines file path for saving and retrieving data
        # based on user name. User's searches will be retrieved and saved
        # under a folder named using self.name as a subdirectory
        # under "src/resources".
        self.path: str = f"resources/{self.name}/"

    def API_key_check(self, file_path: str = ".env") -> bool:
        """Check for user's API key stored in .env file.

        File path must be src/.env for the application to work.

        Args:
            file_path (str): file path to retrieve API_key. Defaults to ".env".

        Returns:
            True if key exists, False if file does not exist.
        """
        key_exist = False
        try:
            with open(file_path, "r") as file:
                content = file.read()
                if "API_KEY" in content:
                    key_exist = True
        except FileNotFoundError:
            key_exist = False
        return key_exist

    def set_API_key(self, file_path: str = ".env"):
        """Saves user's API_KEY to the specified file path.

        Prints instruction for user to obtain API key and subscribe to the
        RapidApi TripAdvisor API, prompt user to enter API_KEY and store
        in the src/.env folder to be accessed as a persistent environment
        variable. Program will restart once this is saved. This file is
        not saved in git.

        Args:
            file_path (str): file path to save API_key. Defaults to ".env".
        """
        print("""
    You can obtain an API key when you sign up
    and subscribe to the Tripadvisor API on RapidAPI.
    URL: https://rapidapi.com/apidojo/api/tripadvisor1
    """)
        user_key: str = input("Please enter your API key here\n")
        with open(file_path, "w") as file:
            file.write(f"API_KEY={user_key}")
        print("API key saved.")
        # Program restarts after API_key is saved in order to access .env
        python = sys.executable
        os.execl(python, python, *sys.argv)
