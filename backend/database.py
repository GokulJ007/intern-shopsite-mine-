import os
import pymysql
import pymysql.cursors
from dotenv import load_dotenv

# Load env variables (in case database.py is imported directly elsewhere)
load_dotenv()

def DB_connection():
    try:
        connector = pymysql.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            database=os.getenv('DB_NAME', 'defaultdb'),
            port=int(os.getenv('DB_PORT', 3306)),
            ssl={'ssl_mode': 'REQUIRED'},
            cursorclass=pymysql.cursors.DictCursor,
        )
        return connector
    except pymysql.MySQLError as e:
        raise Exception("error in connecting to db") from e
