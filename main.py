import os
from dotenv import load_dotenv
from app.testConnection import test_conn
from database.dbconntest import db_test

load_dotenv()  # This IS at the root level now, so should work

if __name__ == "__main__":
    apitest = test_conn()
    dbtest = db_test()
    if dbtest:
        print("success")
