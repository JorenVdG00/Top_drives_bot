import json

import psycopg2
import os
from psycopg2 import sql
from dotenv import load_dotenv

load_dotenv()


def get_db_connection():
    """Establishes and returns a connection to the PostgreSQL Database."""
    conn = psycopg2.connect(
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT')
    )
    return conn

