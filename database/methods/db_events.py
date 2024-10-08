import os
from database.db_general import get_db_connection
from ImageTools.utils.file_utils import delete_dir
from datetime import datetime
from config import BASE_DIR


def reload_events():
    conn = get_db_connection()
    cursor = conn.cursor()
    EVENT_IMG_DIR = os.path.join(BASE_DIR, 'database', 'temp')
    try:
        print('RELOADING EVENTS')
        # Get All events that expired
        cursor.execute("""
        SELECT event_name FROM events
        WHERE end_time < %s AND ended = FALSE;
        """, (datetime.now(),))
        event_names = cursor.fetchall()
        for event_tuple in event_names:
            event_name = event_tuple[0]  # Extract the event name from the tuple
            event_dir_path = os.path.join(EVENT_IMG_DIR, event_name)
            delete_dir(event_dir_path)

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


def get_most_recent_club_reqs():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT time_added
            FROM club_reqs
            order by time_added desc limit 1;
            """)
        time = cursor.fetchone()
        if time:
            time_added = time[0]
            return time_added
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
            WHERE event_name = %s AND ended = FALSE;
            """, (event_name,))

        event_id = cursor.fetchone()
        if event_id:
            return event_id[0]
        else:
            print(f"No event found with name '{event_name}'.")
            if event_name:
                similar_event_name = get_similar_event_names(event_name.upper())
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
            SELECT event_name, event_dir, end_time FROM events
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
            SELECT track_serie_id FROM track_serie
            WHERE track_set_id IN (SELECT track_set_id FROM track_set
            WHERE event_id = %s);
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


def get_club_track_set_of_name(track_set_name):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
        SELECT club_set_id from club_track_set where track_set_name = %s;""", (track_set_name,))

        club_track_sets = cursor.fetchone()
        if club_track_sets:
            club_track_sets = club_track_sets[0]
            return club_track_sets

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
            SELECT event_id FROM track_set
            WHERE track_set_id IN (SELECT track_set_id FROM track_serie
            WHERE track_serie_id = '%s');
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


def get_races(track_serie_id):
    std_condition_dict = {'SUN': False, 'WET': False, 'HIGH': False, 'ROLLING': False}

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
             SELECT race_id, race_name, road_type, conditions, race_number FROM races
             WHERE track_serie_id = '%s'
             ORDER BY race_number ASC;
        """, (track_serie_id,))

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
            print(f"No race found for series ID {track_serie_id}.")
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
        SELECT serie_number FROM track_serie
        WHERE track_serie_id = %s;
        """, (series_id,))

        serie_number = cursor.fetchone()
        if serie_number:
            return serie_number[0]

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        cursor.close()
        conn.close()


def get_serie_id_from_track_set_id(track_set_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
        SELECT track_serie_id From track_serie
        WHERE track_set_id = %s;
        """, (track_set_id,))

        serie_ids = cursor.fetchall()
        serie_id_list = []
        if serie_ids:
            for serie_id in serie_ids:
                serie_id_list.append(serie_id[0])
            return serie_id_list
        else:
            return None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        cursor.close()
        conn.close()


def get_track_set_from_serie(series_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
        SELECT track_set_id From track_serie
        WHERE track_serie_id = %s;""", (series_id,))

        track_set_id = cursor.fetchone()
        if track_set_id:
            return track_set_id[0]
        else:
            return None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        cursor.close()
        conn.close()


def get_assignees(track_serie_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    if not track_serie_id:
        return None
    try:
        cursor.execute("""
        SELECT r.race_number, ca.car_number FROM races r 
        JOIN car_assignments ca ON r.race_id = ca.race_id
        WHERE r.track_serie_id = %s
        ORDER BY r.race_number ASC;""", (track_serie_id,))

        assignees = cursor.fetchall()
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


def get_track_set(track_set_name):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
        SELECT club_set_id From club_track_set
        WHERE track_set_name = %s;
        """, (track_set_name,))

        track_set_id = cursor.fetchone()
        if track_set_id:
            return track_set_id[0]

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        cursor.close()
        conn.close()


def get_club_from_name(club_name):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
        SELECT club_id From club_event
        WHERE club_name = %s;
        """, (club_name,))
        club_id = cursor.fetchone()
        if club_id:
            return club_id[0]

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        cursor.close()
        conn.close()


def get_req_id(req):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""SELECT club_req_id FROM club_reqs
        WHERE req = %s;""", (req,))

        club_req_id = cursor.fetchone()
        if club_req_id:
            return club_req_id[0]
        return None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        cursor.close()
        conn.close()


def play_club_event(club_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
        UPDATE club_event
        SET played_matches = played_matches + 1
        where club_id = %s;""", (club_id,))

        conn.commit()

        club_event = cursor.fetchone()
        if club_event:
            return club_event[0]

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        cursor.close()
        conn.close()


def get_req_num(req_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""SELECT req_number from club_reqs WHERE club_req_id = %s""",
                       (req_id,))
        req_num = cursor.fetchone()
        if req_num:
            return req_num[0]
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        cursor.close()
        conn.close()


def get_req_list(club_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Corrected query to check for club_req1_id or club_req2_id
        cursor.execute("""
            SELECT req_number 
            FROM club_reqs
            WHERE club_req_id IN (
                SELECT club_req1_id FROM club_event WHERE club_id = %s
                UNION
                SELECT club_req2_id FROM club_event WHERE club_id = %s
            )
        """, (club_id, club_id))
        club_req_list = cursor.fetchall()
        print(club_req_list)
        if len(club_req_list) > 1:
            req_num1, req_num2 = club_req_list[0], club_req_list[1]

        elif len(club_req_list) == 1:
            req_num1, req_num2 = club_req_list[0], 0

        else:
            req_num1, req_num2 = 0, 0
        req_list = generate_req_list(req_num1, req_num2)
        return req_list
    except Exception as e:
        print(f"An error occurred with req_list: {e}")
        return None
    finally:
        cursor.close()
        conn.close()



def generate_req_list(req1_num, req2_num):
    req_list = []

    # Fill the req_list with req1 requirements
    for _ in range(req1_num):
        req_list.append([1])

    # Merge or add req2 requirements
    if req2_num:
        if req1_num == 5:
            # Merge req2 into req1
            for i in range(min(req1_num, req2_num)):
                req_list[i].append(2)
            # If req2_num exceeds req1_num, append additional lists for remaining req2
            for i in range(req1_num, req1_num + (req2_num - req1_num)):
                req_list.append([2])
        else:
            # Add req2 as new lists
            for _ in range(req2_num):
                req_list.append([2])

    return req_list


def get_played_matches(club_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""SELECT played_matches From club_event WHERE club_id = %s""", (club_id,))

        played_matches = cursor.fetchone()
        if played_matches:
            return played_matches[0]
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        cursor.close()
        conn.close()


def get_active_club():
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""SELECT club_id From club_event WHERE ended = FALSE""")
        club_id = cursor.fetchone()
        if club_id:
            return club_id[0]
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        cursor.close()
        conn.close()


def end_active_club():
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""UPDATE club_event
         SET ended = TRUE WHERE ended = FALSE""")

        conn.commit()
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
