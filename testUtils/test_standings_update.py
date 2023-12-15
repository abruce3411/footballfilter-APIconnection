import psycopg2
from psycopg2.extras import execute_values
import os
from loguru import logger
import sys
import json

logger.add("central.log", rotation="5 MB", level="INFO")
logger.add("error.log", rotation="10 MB", level="ERROR")
logger.configure(
    handlers=[
        {"sink": "error.log", "level": "ERROR"},
        {"sink": "central.log", "level": "INFO"},
        {"sink": sys.stdout, "level": "DEBUG", "colorize": True},
    ]
)


def read_standings_from_json():
    """Reads standings data from team_rankings.json.

    Returns:
        list: List of standings dictionaries, or None on error
    """

    try:
        with open("team_rankings.json", "r") as f:
            print(f)
            return json.load(f)
    except FileNotFoundError:
        logger.error("team_rankings.json file not found.")
        return None
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing team_rankings.json: {e}")
        return None


def update_standings_test(fetched_standings=None):
    """Bulk inserts or updates standings data in the database.

    Args:
        fetched_standings (list, optional): List of standings dicts to process.
            If not provided, will read from team_rankings.json.

    Returns:
        int: Number of rows inserted, or None on error (exception not raised)
    """

    if fetched_standings is None:
        fetched_standings = read_standings_from_json()
        if fetched_standings is None:
            return None  # Indicate error if reading from JSON failed

    try:
        conn = psycopg2.connect(
            host=os.getenv("dbhost"),
            database=os.getenv("database"),
            user=os.getenv("user"),
            password=os.getenv("password"),
        )
        logger.info("Database connection established successfully.")
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return None

    try:
        insert_query = """
        INSERT INTO league_standings (league_id, rank, team_name, points, goalsDiff, played, form, goals_for, goals_against, wins, draws, losses)
        VALUES %s
        """
        value_tuples = [
            (
                standing["league_id"],
                standing["rank"],
                standing["team_name"],
                standing["points"],
                standing["goalsDiff"],
                standing["played"],
                standing["form"],
                standing["goals_for"],
                standing["goals_against"],
                standing["wins"],
                standing["draws"],
                standing["losses"],
            )
            for standing in fetched_standings
        ]

        with conn.cursor() as cursor:
            result = execute_values(cursor, insert_query, value_tuples)
            conn.commit()
            logger.success("Bulk insert/update successful")
            return result
    except Exception as e:
        logger.error(f"Bulk insert/update failed: {e}")
        logger.error(f"Failed query: {insert_query}")
        if value_tuples:  # Check if value_tuples is not empty
            logger.error(f"Failed data: {value_tuples}")
    finally:
        conn.close()
