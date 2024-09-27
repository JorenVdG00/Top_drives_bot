from OLD.Database.db_general import get_db_connection


def assign_car_to_race(race_id, car_number):
    """Assign a car to a race."""
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # First, delete any existing assignments for this race_id
        cursor.execute("""
            DELETE FROM car_assignments WHERE race_id = %s;
        """, (race_id,))

        cursor.execute("""
            INSERT INTO car_assignments (race_id, car_number)
            VALUES (%s, %s)
            ON CONFLICT (race_id, car_number) DO NOTHING;
            """, (race_id, car_number))

        conn.commit()
        print(f"Car {car_number} assigned to race {race_id}.")
    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()
