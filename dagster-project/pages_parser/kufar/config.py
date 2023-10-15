import os
from dotenv import load_dotenv

load_dotenv()

# Paths
EXECUTABLE_PATH = os.getenv("EXECUTABLE_PATH")
URL_KUFAR = os.getenv("URL_KUFAR")
API_URL_KUFAR = os.getenv("API_URL_KUFAR")


HEADERS = {
        "Host": "api.kufar.by",
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/118.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/json'
    }
