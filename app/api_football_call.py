import requests
from dotenv import load_dotenv
import os
import json


def apiCall():
    load_dotenv()

    url = "https://api-football-v1.p.rapidapi.com/v3/standings"

    querystring = {"season": "2023", "league": "39"}

    headers = {
        "X-RapidAPI-Key": os.getenv("RAPIDAPI_KEY"),
        "X-RapidAPI-Host": os.getenv("RAPIDAPI_Host"),
    }

    try:
        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status()  # Raise error for unsuccessful status codes
    except requests.exceptions.RequestException as err:
        print(f"Error occurred during API call: {err}")
        return None

    try:
        data = response.json()
    except ValueError as err:
        print(f"Error occurred while parsing JSON data: {err}")
        return None

    standings = data["response"][0]["league"]["standings"][0]
    teams = {}
    for team in standings:
        rank = team["rank"]
        team_name = team["team"]["name"]
        teams[str(rank)] = team_name

    with open("team_rankings.json", "w") as outfile:
        json.dump(teams, outfile, indent=4)

    return data


if __name__ == "__main__":
    league_data = apiCall()
