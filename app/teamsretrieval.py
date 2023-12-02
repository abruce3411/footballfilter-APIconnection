import requests
from dotenv import load_dotenv
import os
import json


def get_teams(season):
    load_dotenv()

    url = "https://api-football-v1.p.rapidapi.com/v3/teams"

    querystring = {"league": str(39), "season": str(season)}

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

    # Extract and format information from each team

    filtered_teams = []

    for team_data in data["response"]:
        team_info = {
            "id": team_data["team"]["id"],
            "name": team_data["team"]["name"],
            "code": team_data["team"]["code"],
            "stadium": team_data["venue"]["name"],
            "stadium_city": team_data["venue"]["city"],
        }
        filtered_teams.append(team_info)

    data = filtered_teams

    with open("team_info.json", "w") as output:
        json.dump(filtered_teams, output, indent=1)

    return data


if __name__ == "__main__":
    league_id = 39
    season = 2023
    team_data = get_teams(league_id, season)
