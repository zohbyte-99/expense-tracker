import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
def get_connection():
    conn=psycopg2.connect(
        host=os.getenv("db_host"),
        database=os.getenv("db_database"),
        user=os.getenv("db_user"),
        password=os.getenv("db_password"),
        port=os.getenv("db_port")
    )
    return conn