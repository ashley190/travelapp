from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())
key = os.getenv("API_KEY")
print(key)
