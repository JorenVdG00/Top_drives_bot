from database.db_general import get_db_connection
import json


def add_event(event_name, event_dir, end_time):
    """Inserts a new event into the database."""
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO events (event_name, event_dir, end_time)
            VALUES (%s, %s, %s)
            RETURNING event_id;
            """, (event_name, event_dir, end_time))

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


def add_series(event_id, serie_number):
    """Inserts a new series into the database."""
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        print("series: "+ str(event_id))

        cursor.execute("""
            INSERT INTO series (event_id, serie_number)
            VALUES (%s, %s)
            RETURNING series_id;
            """, (str(event_id), serie_number))
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