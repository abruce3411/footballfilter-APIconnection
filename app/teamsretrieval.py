from loguru import logger
from dotenv import load_dotenv
import os
import json
import requests
import sys

logger.add("team_retrieval.log", rotation="5 MB", level="INFO")
logger.add("error.log", rotation="10 MB", level="ERROR")
logger.configure(
    handlers=[
        {"sink": "error.log", "level": "ERROR"},
        {"sink": "team_retrieval.log", "level": "INFO"},
        {"sink": sys.stdout, "level": "DEBUG", "colorize": True},
    ]
)


def get_teams(season):
    load_dotenv()
    logger.debug("give me my logs")
    url = "https://api-football-v1.p.rapidapi.com/v3/teams"

    querystring = {"league": str(39), "season": str(season)}

    headers = {
        "X-RapidAPI-Key": os.getenv("RAPIDAPI_KEY"),
        "X-RapidAPI-Host": os.getenv("RAPIDAPI_Host"),
    }
    logger.info("Retrieving team information for season {}".format(season))
    try:
        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status()  # Raise error for unsuccessful status codes
        logger.success("Retrieved team data successfully")
    except requests.exceptions.RequestException as err:
        logger.error("Error occurred during API call: {}".format(err))
        return None

    try:
        data = response.json()
        logger.info(f"Processed team information: {data}")
    except ValueError as err:
        logger.error(f"Error occurred during data processing: {err}")
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
    logger.info("Logs")
    league_id = 39
    season = 2023
    try:
        team_data = get_teams(season, league_id)
    except:
        logger.error("RUNTIME ERROR TEST SUCCESSFUL - BAD ARGS")
