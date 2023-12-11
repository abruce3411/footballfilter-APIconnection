import requests
from dotenv import load_dotenv
import os
import json
from loguru import logger
from constantUtils import constants  # Import constants module
import sys

logger.add("central.log", rotation="5 MB", level="INFO")
logger.add("error.log", rotation="10 MB", level="ERROR")
logger.configure(
    handlers=[
        {"sink": "error.log", "level": "ERROR"},
        {"sink": "central.log", "level": "INFO"},
        {"sink": sys.stdout, "level": "DEBUG", "colorize": True},
    ]
)


def get_standings(season):
    load_dotenv()

    url = "https://api-football-v1.p.rapidapi.com/v3/standings"

    all_standings_data = []

    # Iterate through each league and make API calls
    for league in constants.LEAGUES:
        querystring = {
            "season": str(season),
            "league": str(league.id),
        }
        headers = {
            "X-RapidAPI-Key": os.getenv("RAPIDAPI_KEY"),
            "X-RapidAPI-Host": os.getenv("RAPIDAPI_Host"),
        }

        logger.info(
            "Retrieving standings for league {} and season {}".format(
                league.name, season
            )
        )
        try:
            response = requests.get(url, headers=headers, params=querystring)
            response.raise_for_status()  # Raise error for unsuccessful status codes
            logger.success(
                "Retrieved standings data successfully for league {}".format(
                    league.name
                )
            )

            # Process the response data
            data = response.json()
            logger.info(f"Processed standings data: {data}")
            league_id = data["parameters"]["league"]

            # Extract and format standings for each team
            filtered_standings = []
            standings = data["response"][0]["league"]["standings"][0]
            for team in standings:
                rank = team["rank"]
                team_name = team["team"]["name"]
                points = team["points"]
                goals_diff = team["goalsDiff"]
                played = team["all"]["played"]
                form = team["form"]

                team_info = {
                    "league_id": league_id,
                    "rank": rank,
                    "team_name": team_name,
                    "points": points,
                    "goalsDiff": goals_diff,
                    "played": played,
                    "form": form,
                }
                filtered_standings.append(team_info)
            # Add standings to the combined list
            all_standings_data.extend(filtered_standings)

            # Write filtered standings to JSON file (optional for debugging)
            with open("team_rankings.json", "a") as output:
                json.dump(filtered_standings, output, indent=1)
                output.write("\n")

        except (requests.exceptions.RequestException, ValueError) as err:
            logger.error(
                "Error occurred during API call or data processing for league {}: {}".format(
                    league.name, err
                )
            )
            return None

    return all_standings_data


if __name__ == "__main__":
    league_data = get_standings()
