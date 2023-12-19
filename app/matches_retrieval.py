from loguru import logger
from dotenv import load_dotenv
import os
import json
import requests
import sys
from constantUtils import constants  # Assuming this holds your constants

# Logging configuration (same as your teams module)
logger.add("central.log", rotation="5 MB", level="INFO")
logger.add("error.log", rotation="10 MB", level="ERROR")
logger.configure(
    handlers=[
        {"sink": "error.log", "level": "ERROR"},
        {"sink": "central.log", "level": "INFO"},
        {"sink": sys.stdout, "level": "DEBUG", "colorize": True},
    ]
)


def get_matches(season):
    load_dotenv()
    logger.debug("Logging enabled.")

    all_matches_data = []

    # Iterate through leagues and rounds
    for league in constants.LEAGUES:
        round_number = 1
        querystring = {
            "league": str(league.id),
            "round": "Regular Season - " + str(round_number),
            "season": str(season),
        }
        headers = {
            "X-RapidAPI-Key": os.getenv("RAPIDAPI_KEY"),
            "X-RapidAPI-Host": os.getenv("RAPIDAPI_Host"),
        }

        logger.info(
            "Retrieving match info for league {} round {} season {}".format(
                league.name, round_number, season
            )
        )
        try:
            url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
            response = requests.get(url, headers=headers, params=querystring)
            response.raise_for_status()
            logger.success(
                "Retrieved match data successfully for league {} round {}".format(
                    league.name, round_number
                )
            )

            data = response.json()
            logger.info(f"Processed match info: {data}")

            for match in data.get("response", []):
                match_info = {
                    "league_id": league.id,
                    "stadium": match["fixture"]
                    .get("venue", {})
                    .get("name"),  # Access venue within fixture
                    "date": match["fixture"]["date"][:10],
                    "referee": match["fixture"].get("referee"),
                    "round": round_number,
                    "winner": match["teams"]["away"]["name"]
                    if match["teams"]["away"]["winner"]
                    else match["teams"]["home"]["name"],
                    "loser": match["teams"]["home"]["name"]
                    if match["teams"]["away"]["winner"]
                    else match["teams"]["away"]["name"],
                    "goals_home": match["goals"]["home"],
                    "goals_away": match["goals"]["away"],
                    "match_id": match["fixture"]["id"],
                }
                all_matches_data.append(match_info)
            with open("matches_info.json", "w") as output:
                json.dump(all_matches_data, output, indent=1)
        except (requests.exceptions.RequestException, ValueError) as err:
            logger.error(
                f"Error during API call or data processing for league {league.name} round {round_number}: {err}"
            )

    return all_matches_data
