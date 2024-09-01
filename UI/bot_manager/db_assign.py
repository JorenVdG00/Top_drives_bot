from database.db_car_assign import assign_car_to_race

def save_car_assignments_to_db(car_assignments):
    for race_number, car_number in car_assignments:
        # Replace with actual database insertion logic
        assign_car_to_race(race_number, car_number)
        print(f'Saving Car {car_number} assignment for Race {race_number} to DB')
