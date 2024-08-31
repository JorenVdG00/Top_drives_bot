import json

import psycopg2
import os
from psycopg2 import sql
from dotenv import load_dotenv

load_dotenv()


def get_db_connection():
    """Establishes and returns a connection to the PostgreSQL database."""
    conn = psycopg2.connect(
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT')
    )
    return conn


def add_event(event_name, end_time):
    """Inserts a new event into the database."""
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO events (event_name, end_time)
            VALUES (%s, %s)
            RETURNING event_id;
            """, (event_name, end_time))

        event_id = cursor.fetchone()[0]
        conn.commit()
        print(f"Event '{event_name}' added with ID {event_id}.")
        return event_id
    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


def add_series(event_id):
    """Inserts a new series into the database."""
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        print("series: "+ str(event_id))

        cursor.execute("""
            INSERT INTO series (event_id)
            VALUES (%s)
            RETURNING series_id;
            """, (str(event_id)))
        series_id = cursor.fetchone()[0]
        conn.commit()
        print(f"Serie '{series_id}' added with FK_ID {event_id}.")
        return series_id
    except Exception as e:
        print(f"An error occurred in series: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


def add_race(race_name, road_type, conditions, race_number, series_id):
    """Inserts a new race into the database."""
    conn = get_db_connection()
    cursor = conn.cursor()

    try:

        conditions_json = json.dumps(conditions)
        cursor.execute("""
            INSERT INTO races (race_name, road_type, conditions, race_number, series_id)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING race_id;
            """, (race_name, road_type, conditions_json, race_number, series_id))

        race_id = cursor.fetchone()[0]
        conn.commit()
        print(f"Race '{race_name}' added with ID {race_id}.")
        return race_id
    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()
