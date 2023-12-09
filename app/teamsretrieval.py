from loguru import logger
from dotenv import load_dotenv
import os
import json
import requests
import sys
from constantUtils import constants

logger.add("central.log", rotation="5 MB", level="INFO")
logger.add("error.log", rotation="10 MB", level="ERROR")
logger.configure(
    handlers=[
        {"sink": "error.log", "level": "ERROR"},
        {"sink": "central.log", "level": "INFO"},
        {"sink": sys.stdout, "level": "DEBUG", "colorize": True},
    ]
)


def get_teams(season):
    load_dotenv()
    logger.debug("give me my logs")
    url = "https://api-football-v1.p.rapidapi.com/v3/teams"

    all_teams_data = []

    # Iterate through each league and make API calls
    for league in constants.LEAGUES:
        querystring = {"league": str(league.id), "season": str(season)}
        headers = {
            "X-RapidAPI-Key": os.getenv("RAPIDAPI_KEY"),
            "X-RapidAPI-Host": os.getenv("RAPIDAPI_Host"),
        }

        logger.info(
            "Retrieving team information for league {} and season {}".format(
                league.name, season
            )
        )
        try:
            response = requests.get(url, headers=headers, params=querystring)
            response.raise_for_status()  # Raise error for unsuccessful status codes
            logger.success(
                "Retrieved team data successfully for league {}".format(league.name)
            )

            # Process the response data
            data = response.json()
            logger.info(f"Processed team information: {data}")

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

            # Add teams to the combined list
            all_teams_data.extend(filtered_teams)

            # Write filtered teams to JSON file (optional for debugging)
            with open("team_info.json", "a") as output:
                json.dump(filtered_teams, output, indent=1)
                output.write("\n")

        except (requests.exceptions.RequestException, ValueError) as err:
            logger.error(
                "Error occurred during API call or data processing for league {}: {}".format(
                    league.name, err
                )
            )
            return None

    return all_teams_data


if __name__ == "__main__":
    get_teams(2023)
