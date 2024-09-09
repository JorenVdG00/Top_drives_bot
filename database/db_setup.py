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
            event_dir VARCHAR(255) NOT NULL,
            ended BOOLEAN DEFAULT FALSE
            );
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS club_track_set (
        club_set_id SERIAL PRIMARY KEY,
        track_set_name VARCHAR(255) NOT NULL,
        active BOOLEAN DEFAULT FALSE 
        );""")

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS track_set (
        track_set_id SERIAL PRIMARY KEY,
        event_id INTEGER REFERENCES events(event_id) ON DELETE CASCADE DEFAULT NULL ,
        club_set_id INTEGER REFERENCES club_track_set(club_set_id) ON DELETE CASCADE DEFAULT NULL 
        );
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS track_serie (
        track_serie_id SERIAL PRIMARY KEY,
        serie_number INTEGER NOT NULL,
        track_set_id INTEGER REFERENCES track_set (track_set_id) ON DELETE CASCADE
        );
        """)

        cursor.execute("""
           CREATE TABLE IF NOT EXISTS races (
               race_id SERIAL PRIMARY KEY,
               race_name VARCHAR(255) NOT NULL,
               road_type VARCHAR(255) NOT NULL,
               conditions JSONB,  -- JSONB column to store conditions as key-value pairs
               race_number INTEGER NOT NULL,
               track_serie_id INTEGER REFERENCES track_serie(track_serie_id) ON DELETE CASCADE

           );
           """)
        # cursor.execute("""
        # CREATE TABLE IF NOT EXISTS series (
        #     series_id SERIAL PRIMARY KEY,
        #     serie_number INTEGER NOT NULL,
        #     event_id INTEGER REFERENCES events(event_id),
        #     track_serie_id INTEGER REFERENCES track_serie(track_serie_id)
        #     );
        # """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS car_assignments (
            assignment_id SERIAL PRIMARY KEY,
            race_id INTEGER REFERENCES races(race_id) ON DELETE CASCADE, 
            car_number INTEGER NOT NULL, -- This will store car numbers (1-5)
            UNIQUE(race_id, car_number)  -- Ensure each car can only be assigned to a race once
        );

        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS club_reqs (
        club_req_id SERIAL PRIMARY KEY,
        req VARCHAR(255),
        req_number INTEGER
        );
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS club_event (
            club_id SERIAL PRIMARY KEY,
            club_name VARCHAR(255) NOT NULL,
            played_matches INTEGER default 1,
            ended BOOLEAN DEFAULT FALSE,       
            rq INTEGER NOT NULL,
            club_set_id INTEGER REFERENCES club_track_set(club_set_id),
            club_req1_id INTEGER REFERENCES club_reqs(club_req_id)
            club_req2_id INTEGER REFERENCES club_reqs(club_req_id)
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


def delete_tables():
    """Deletes specific tables from the database."""
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
        DROP TABLE IF EXISTS car_assignments CASCADE;
        DROP TABLE IF EXISTS races CASCADE;
        DROP TABLE IF EXISTS series CASCADE;
        DROP TABLE IF EXISTS events CASCADE;
        DROP TABLE IF EXISTS track_set CASCADE;
        DROP TABLE IF EXISTS track_serie CASCADE;
        DROP TABLE IF EXISTS club_track_set CASCADE;
        DROP TABLE IF EXISTS club_event CASCADE;
        DROP TABLE IF EXISTS club_reqs CASCADE;
        """)

        conn.commit()
        print("Tables deleted successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


def main():
    # Optionally, drop existing tables before creating new ones
    delete_tables()

    # Create tables
    create_tables()


if __name__ == "__main__":
    main()
