from database.db_general import get_db_connection


def get_event_id_by_name(event_name):
    """Retrieves the event_id from the database given an event_name."""
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT event_id
            FROM events
            WHERE event_name = %s;
            """, (event_name,))

        event_id = cursor.fetchone()
        if event_id:
            return event_id[0]
        else:
            print(f"No event found with name '{event_name}'.")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        cursor.close()
        conn.close()


def get_races_by_series_id(series_id):
    """Retrieves all races associated with a given series ID."""
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT race_id, race_name, road_type, conditions, race_number, series_id
            FROM races
            WHERE series_id = %s
            ORDER BY race_number;
            """, (series_id,))

        races = cursor.fetchall()
        if races:
            return [{
                "race_id": r[0],
                "race_name": r[1],
                "road_type": r[2],
                "conditions": r[3],
                "race_number": r[4],
                "series_id": r[5]
            } for r in races]
        else:
            print(f"No races found for series ID {series_id}.")
            return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []
    finally:
        cursor.close()
        conn.close()


def get_series_by_event_id(event_id):
    """Retrieves all series associated with a given event ID."""
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT series_id
            FROM series
            WHERE event_id = %s;
            """, (event_id,))

        series = cursor.fetchall()
        serie_ids = []
        if series:
            [serie_ids.append(s) for s in series]
            return serie_ids
        # if series:
        #     return [{"serie_id": s[0], "event_id": s[1]} for s in series]
        else:
            print(f"No series found for event ID {event_id}.")
            return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []
    finally:
        cursor.close()
        conn.close()


def get_event_by_id(event_id):
    """Retrieves an event from the database by its ID."""
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT event_id, event_name, end_time
            FROM events
            WHERE event_id = %s;
            """, (event_id,))

        event = cursor.fetchone()
        if event:
            return {
                "event_id": event[0],
                "event_name": event[1],
                "end_time": event[2]
            }
        else:
            print(f"No event found with ID {event_id}.")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        cursor.close()
        conn.close()


def get_club_reqs():
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
        SELECT req1, req1_number, req2, req2_number
        FROM club_reqs
        """)
        club_reqs = cursor.fetchall()
        if club_reqs:
            return club_reqs
        else:
            return None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        cursor.close()
        conn.close()
