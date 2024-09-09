from database.db_general import get_db_connection


def remove_event(event_id):
    """Removes all series related to the given event_id from the database."""
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        print(f"Removing all series for event_id: {event_id}")
        # # First, delete from the car_assignments table based on race_ids
        # cursor.execute("""
        #     DELETE FROM car_assignments
        #     WHERE race_id IN (
        #         SELECT race_id FROM races WHERE track_set_id IN (
        #             SELECT track_set_id FROM track_set WHERE event_id = %s
        #         )
        #     );
        # """, (str(event_id),))

        # Now delete from the 'series' table
        cursor.execute("""
            DELETE FROM events
            WHERE event_id = %s;
        """, (str(event_id),))

        conn.commit()
        print(f"All series related to event_id '{event_id}' have been removed.")
    except Exception as e:
        print(f"An error occurred while removing series: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


# def remove_event(event_id):
#     print(f"Removing all events for event_id: {event_id}")
#     conn = get_db_connection()
#     cursor = conn.cursor()
#
#     try:
#         cursor.execute("""
#                 DELETE FROM events
#                 WHERE event_id = %s;
#             """, (event_id,))
#
#         conn.commit()
#         print(f"All series related to event_id '{event_id}' have been removed.")
#     except Exception as e:
#         print(f"An error occurred while removing series: {e}")
#         conn.rollback()
#     finally:
#         cursor.close()
#         conn.close()



def delete_club_reqs():
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
                DELETE FROM club_reqs
            """)

        conn.commit()
    except Exception as e:
        print(f"An error occurred while removing series: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def delete_club_track_sets():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
                DELETE FROM club_track_set
                WHERE club_set_id IN (
                    SELECT club_set_id FROM track_set WHERE club_set_id IS NOT NULL
                );
            """)

        conn.commit()
    except Exception as e:
        print(f"An error occurred while removing series: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()
