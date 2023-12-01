import psycopg2
import os
import dotenv

dotenv.load_dotenv()


class DBWriter:
    def __init__(self):
        self.conn = psycopg2.connect(
            host=os.getenv("dbhost"),
            database=os.getenv("database"),
            user=os.getenv("postgres"),
            password=os.getenv("password"),
        )

    def insert_leagues(self):
        """Inserts multiple leagues into the table at once.

        Args:
            leagues_data: List of tuples, each tuple being (id, name, season_year)
        """
        cursor = self.conn.cursor()
        leagues_data = [
            (1, "Premier League", 2023),
            (2, "La Liga", 2023),
            (3, "Serie A", 2023),
            (4, "Bundesliga", 2023),
            (5, "Ligue 1", 2023),
        ]
        query = "INSERT INTO leagues (id, name, season_year) VALUES %s"
        psycopg2.extras.execute_values(cursor, query, leagues_data)

        self.conn.commit()
        cursor.close()


if __name__ == "__main__":
    db = DBWriter()
    db.insert_leagues()
