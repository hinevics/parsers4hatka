import os

from dotenv import load_dotenv


load_dotenv()

URL_REALT = os.getenv("URL_REALT")
HEADERS = {
        "Host": "api.kufar.by",
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/118.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/json'
    }
URL_REALT_BASE = os.getenv("URL_REALT_BASE")
