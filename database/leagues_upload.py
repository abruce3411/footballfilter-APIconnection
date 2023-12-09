import os
import dotenv
import psycopg2
from psycopg2 import extras

dotenv.load_dotenv()


class DBWriter:
    def __init__(self):
        self.conn = psycopg2.connect(
            host=os.getenv("dbhost"),
            database=os.getenv("database"),
            user=os.getenv("user"),
            password=os.getenv("password"),
        )

    def insert_leagues(self):
        """Inserts multiple leagues into the table at once.

        Args:
            leagues_data: List of tuples, each tuple being (id, name, season_year)
        """
        cursor = self.conn.cursor()
        leagues_data = [
            (39, "Premier League", 2023),
            (140, "La Liga", 2023),
            (135, "Serie A", 2023),
            (78, "Bundesliga", 2023),
            (61, "Ligue 1", 2023),
        ]
        query = """
        INSERT INTO leagues (id, name, season_year) 
        VALUES %s 
        ON CONFLICT (id) DO UPDATE
        SET
        
        """
        psycopg2.extras.execute_values(cursor, query, leagues_data)

        self.conn.commit()
        cursor.close()


if __name__ == "__main__":
    db = DBWriter()
    db.insert_leagues()
