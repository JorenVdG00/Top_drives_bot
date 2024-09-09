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


# def add_series(event_id, serie_number, track_set_id):
#     """Inserts a new series into the database."""
#     conn = get_db_connection()
#     cursor = conn.cursor()
#
#     try:
#         print("series: " + str(event_id))
#
#         cursor.execute("""
#             INSERT INTO series (event_id, serie_number, track_set_id)
#             VALUES (%s, %s, %s)
#             RETURNING series_id;
#             """, (str(event_id), serie_number, track_set_id))
#         series_id = cursor.fetchone()[0]
#         conn.commit()
#         print(f"Serie '{series_id}' added with FK_ID {event_id}.")
#         return series_id
#     except Exception as e:
#         print(f"An error occurred in series: {e}")
#         conn.rollback()
#     finally:
#         cursor.close()
#         conn.close()


def add_track_set(event_id=None, club_set_id=None):
    """Inserts a new race into the database."""
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        if event_id:
            cursor.execute("""
                INSERT INTO track_set (event_id)
                VALUES (%s)
                RETURNING track_set_id
            """, (event_id,))
        elif club_set_id:
            cursor.execute("""
                INSERT INTO track_set (club_set_id)
                VALUES (%s)
                RETURNING track_set_id
            """, (club_set_id,))
        else:
            cursor.execute("""
                INSERT INTO track_set DEFAULT VALUES RETURNING track_set_id;
            """)

        conn.commit()

        track_set_id = cursor.fetchone()[0]
        print(track_set_id)
        return track_set_id
    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback()
        return None
    finally:
        cursor.close()
        conn.close()


def add_track_serie(serie_number, track_set_id):
    """Inserts a new race into the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:

        cursor.execute("""
            INSERT INTO track_serie (serie_number, track_set_id)
            VALUES (%s, %s)
            RETURNING track_serie_id
        """, (serie_number, track_set_id))

        conn.commit()

        track_serie_id = cursor.fetchone()[0]
        return track_serie_id
    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback()
        return None
    finally:
        cursor.close()
        conn.close()


def add_race(race_name, road_type, conditions, race_number, track_serie_id):
    """Inserts a new race into the database."""
    conn = get_db_connection()
    cursor = conn.cursor()

    try:

        conditions_json = json.dumps(conditions)
        cursor.execute("""
            INSERT INTO races (race_name, road_type, conditions, race_number, track_serie_id)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING race_id;
            """, (race_name, road_type, conditions_json, race_number, track_serie_id))

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


def add_club_reqs(req, req_number):
    """Inserts a new event into the database."""
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO club_reqs (req, req_number)
            VALUES (%s, %s)
            RETURNING club_req_id;
            """, (req, req_number))

        club_req = cursor.fetchone()[0]
        conn.commit()
        return club_req
    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


def add_club_track_set(track_set_name):
    """Inserts a new event into the database."""
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO club_track_set (track_set_name)
            VALUES (%s)
            RETURNING club_set_id;
            """, (track_set_name,))

        club_req = cursor.fetchone()[0]
        conn.commit()
        return club_req
    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


def add_club_event(club_name, rq, club_set_id, club_req1_id, club_req2_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO club_event (club_name, rq, club_set_id, club_req1_id, club_req2_id)
            VALUES (%s,%s,%s,%s,%s)
            RETURNING club_set_id;
            """, (club_name, rq, club_set_id, club_req1_id, club_req2_id))

        club_id = cursor.fetchone()[0]
        conn.commit()
        return club_id
    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()