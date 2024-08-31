from db_general import get_db_connection


def create_tables():
    """Creates tables in the database."""
    conn = get_db_connection()
    cursor = conn.cursor()

    try:


        cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            event_id SERIAL PRIMARY KEY,
            event_name VARCHAR(255) NOT NULL,
            end_time TIMESTAMP NOT NULL,
            ended BOOLEAN DEFAULT FALSE);
        """)


        cursor.execute("""
        CREATE TABLE IF NOT EXISTS series (
            series_id SERIAL PRIMARY KEY,
            event_id INTEGER REFERENCES events(event_id))
        """)



        cursor.execute("""
        CREATE TABLE IF NOT EXISTS races (
            race_id SERIAL PRIMARY KEY,
            race_name VARCHAR(255) NOT NULL,
            road_type VARCHAR(255) NOT NULL,
            conditions JSONB,  -- JSONB column to store conditions as key-value pairs
            race_number INTEGER NOT NULL,
            series_id INTEGER REFERENCES series(series_id)
        );

        """)


        cursor.execute("""
        CREATE TABLE IF NOT EXISTS car_assignments (
            assignment_id SERIAL PRIMARY KEY,
            race_id INTEGER REFERENCES races(race_id),
            car_number INTEGER NOT NULL, -- This will store car numbers (1-5)
            UNIQUE(race_id, car_number)  -- Ensure each car can only be assigned to a race once
        );

        """)



        # Commit the changes
        conn.commit()
        print("Tables created successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


def drop_tables():
    """Drops tables from the database."""
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
        DROP TABLE IF EXISTS races;
        DROP TABLE IF EXISTS series;
        DROP TABLE IF EXISTS events;
        DROP TABLE IF EXISTS car_assignments;
        """)

        conn.commit()
        print("Tables dropped successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


def main():
    # Optionally, drop existing tables before creating new ones
    drop_tables()

    # Create tables
    create_tables()


if __name__ == "__main__":
    main()
