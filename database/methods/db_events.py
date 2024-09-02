from database.db_general import get_db_connection
from datetime import datetime


def reload_events():
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Update events where the end_time has passed and ended is False
        cursor.execute("""
            UPDATE events
            SET ended = TRUE
            WHERE end_time < %s AND ended = FALSE;
        """, (datetime.now(),))

        conn.commit()
        print('Events reloaded')
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        cursor.close()
        conn.close()


def get_all_active_events():
    reload_events()
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Update events where the end_time has passed and ended is False
        cursor.execute("""
            SELECT event_id From events
            WHERE ended = FALSE;
        """)

        events = cursor.fetchall()
        event_ids = []
        if events:
            [event_ids.append(e[0]) for e in events]
            print(f'A total of {len(events)} active events')
            return event_ids
        else:
            print('No active events')
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        cursor.close()
        conn.close()


def get_similar_event_names(event_name):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT event_name
            FROM events
            WHERE ended = FALSE;
            """)

        event_names = cursor.fetchall()
        event_list = []
        if event_names:
            [event_list.append(e[0]) for e in event_names]
            for e_name in event_list:
                if event_name in e_name:
                    print(f"Similar event name: {e_name}, Your name: {event_name}")
                    return e_name
        return None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        cursor.close()
        conn.close()


def get_event_id_by_name(event_name):
    """Retrieves the event_id from the database given an event_name."""
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT event_id
            FROM events
            WHERE event_name = %s and ended = FALSE;
            """, (event_name,))

        event_id = cursor.fetchone()
        if event_id:
            return event_id[0]
        else:
            print(f"No event found with name '{event_name}'.")
            if event_name:
                similar_event_name = get_similar_event_names(event_name)
                if similar_event_name:
                    event_id = get_event_id_by_name(similar_event_name)
                    if event_id:
                        return event_id

        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        cursor.close()
        conn.close()


def get_active_event(event_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT event_name, event_dir, end_time From events
            WHERE event_id = %s;
        """, (event_id,))

        events = cursor.fetchall()
        if len(events) > 0:
            event_name = events[0][0]
            event_dir = events[0][1]
            end_time = events[0][2]
            return event_name, event_dir, end_time
        else:
            return None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        cursor.close()
        conn.close()


def get_series(event_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT series_id From series
            WHERE event_id = %s;
   """, (event_id,))

        series = cursor.fetchall()
        serie_ids = []
        if series:
            [serie_ids.append(s[0]) for s in series]
            return serie_ids
        else:
            print(f"No series found for event ID {event_id}.")
            return None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        cursor.close()
        conn.close()


def get_event_from_serie_id(series_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT event_id From series
            WHERE series_id = %s;
   """, (series_id,))

        event = cursor.fetchone()
        event_id = event[0]
        if event_id:
            return event_id
        else:
            print(f"No series found for event ID {series_id}.")
            return None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        cursor.close()
        conn.close()


def get_races(series_id):
    std_condition_dict = {'SUN': False, 'WET': False, 'HIGH': False, 'ROLLING': False}

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
             SELECT race_id, race_name, road_type, conditions, race_number From races
             WHERE series_id = %s
             ORDER BY race_number ASC;
        """, (series_id,))

        races = cursor.fetchall()

        races_dict = {}
        if races:
            for race in races:
                for condition, bool in race[3].items():
                    if bool:
                        if condition in std_condition_dict:
                            std_condition_dict[condition] = True

                races_dict[race[0]] = {'name': race[1], 'road_type': race[2], 'conditions': std_condition_dict,
                                       'number': race[4]}
            return races_dict
        else:
            print("No race found for series ID {serie_id}.")
        return None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        cursor.close()
        conn.close()


def get_serie_number(series_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
        SELECT serie_number From series
        WHERE series_id = %s;""", (series_id,))

        serie_number = cursor.fetchone()
        if serie_number:
            return serie_number[0]

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        cursor.close()
        conn.close()


def get_assignees(series_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
        SELECT r.race_number, ca.car_number FROM races r 
        JOIN car_assignments ca ON r.race_id = ca.race_id
        WHERE r.series_id = %s
        ORDER BY r.race_number ASC;""", (series_id,))

        assignees = cursor.fetchall()
        print(assignees)
        assignees_dict = {}
        if assignees:
            for r in assignees:
                assignees_dict[r[0]] = r[1]
        return assignees


    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        cursor.close()
        conn.close()


if __name__ == '__main__':
    event_id = get_event_id_by_name("NEW_FOREST_GRAND_PRI")
    print(event_id)
    # print(f'{get_assignees(6)}\n')
    # race_dict = get_races(3)
    # if race_dict:
    #     for race_id, race in race_dict.items():
    #         print(f'Race ID: {race_id}')
    #         print(f'Race name: {race["name"]}')
    #         print(f'Race road type: {race["road_type"]}')
    #         print(f'Race conditions: {race["conditions"]}')
    #         print(f'Race number: {race["number"]}\n')
    # # events = get_all_active_events()
    # # for event in events:
    # #     print(event)
    # # series = get_series(1)
    # # for serie in series:
    # #     print(serie)