from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(dotenv_path=os.path.abspath('.env'))
key = os.getenv("API_KEY")
print(key)
