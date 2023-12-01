import psycopg2
import json, os
import dotenv


def db_test():
    dotenv.load_dotenv()
    try:
        connection = psycopg2.connect(
            database=os.getenv("database"),
            host=os.getenv("dbhost"),
            user=os.getenv("user"),
            password=os.getenv("password"),
        )
        return connection
    except (Exception, psycopg2.Error) as error:
        print("Error connection to PostgreSQL")
        return None


if __name__ == "__main__":
    conn = db_test()
    if conn:
        print("Success")
