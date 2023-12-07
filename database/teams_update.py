import psycopg2
from psycopg2.extras import execute_values
import dotenv
import os
import sys
from loguru import logger

dotenv.load_dotenv()

logger.add("central.log", rotation="5 MB", level="INFO")
logger.add("error.log", rotation="10 MB", level="ERROR")
logger.configure(
    handlers=[
        {"sink": "error.log", "level": "ERROR"},
        {"sink": "team_retrieval.log", "level": "INFO"},
        {"sink": sys.stdout, "level": "DEBUG", "colorize": True},
    ]
)


def bulk_insert_teams(fetched_teams):
    """Bulk inserts team data into the DB, adding hardcoded league_id.
    Args:
        fetched_teams (list): List of team dicts, each with keys for
            'id', 'name', 'code', 'stadium', 'stadium_city' as returned by get_teams
    Returns:
        int: Number of rows inserted, or None on error (exception not raised)
    """

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
            INSERT INTO teams (league_id, id, name, code, stadium, stadium_city)
            VALUES %s
        """

        value_tuples = [
            (
                39,
                team["id"],
                team["name"],
                team["code"],
                team["stadium"],
                team["stadium_city"],
            )
            for team in fetched_teams
        ]

        with conn.cursor() as cursor:
            result = execute_values(cursor, insert_query, value_tuples)
            conn.commit()
            logger.info(f"Bulk insert successful, inserted {result.rowcount} rows.")
            return result.rowcount
    except Exception as e:
        logger.error(f"Bulk insert failed: {e}")
    finally:
        conn.close()
