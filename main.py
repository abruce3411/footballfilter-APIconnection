import os
from dotenv import load_dotenv
from app.testConnection import test_conn

load_dotenv()  # This IS at the root level now, so should work

if __name__ == "__main__":
    data = test_conn()
