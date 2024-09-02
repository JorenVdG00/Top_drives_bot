from database.db_general import get_db_connection


def remove_event_series(event_id):
    """Removes all series related to the given event_id from the database."""
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        print(f"Removing all series for event_id: {event_id}")

        # Assuming you have foreign key constraints, you may need to delete from child tables first.
        # For example, if there's a 'sub_series' table related to 'series':
        cursor.execute("""
            DELETE FROM races
            WHERE series_id IN (
                SELECT series_id FROM series WHERE event_id = %s
            );
        """, (str(event_id),))

        # Now delete from the 'series' table
        cursor.execute("""
            DELETE FROM series
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


def remove_event(event_id):
    remove_event_series(event_id)
    print(f"Removing all events for event_id: {event_id}")
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
                DELETE FROM events
                WHERE event_id = %s;
            """, (event_id,))

        conn.commit()
        print(f"All series related to event_id '{event_id}' have been removed.")
    except Exception as e:
        print(f"An error occurred while removing series: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()