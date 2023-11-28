import requests
import os


def test_conn():
    url = "https://api-football-v1.p.rapidapi.com/v3/timezone"

    headers = {
        "X-RapidAPI-Key": os.getenv("RAPIDAPI_KEY"),
        "X-RapidAPI-Host": os.getenv("RAPIDAPI_HOST"),
    }

    response = requests.get(url, headers=headers)

    print(response.json())
    return response.json()
