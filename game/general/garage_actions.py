import time
from game.general.general_actions import (
    swipe_left_cars,
    tap_garage_car,
    tap_exit_car,
    tap_add_to_hand,
)
from game.general.general_checks import (
    get_nr_available_cars,
    check_add_to_hand,
    check_is_fusing,
    check_is_servicing,
    check_missing_slots,
)


def add_car_to_hand(tries: int = 0) -> bool:
    """
    Tries to add a car to the hand based on the current attempt number.

    Args:
        tries (int): The number of tries attempted to add a car.

    Returns:
        bool: True if the car is successfully added, False otherwise.
    """
    # Swipe left after every 6 tries
    if tries % 6 == 0 and tries != 0:
        swipe_left_cars()

    # Calculate which car to tap
    nr = tries % 6
    x = (nr // 2) + 1
    y = 2 if nr % 2 != 0 else 1
    
    available_cars = get_nr_available_cars()
    if nr+1 > available_cars:
        return False

    # Interact with the car
    tap_garage_car(x, y)
    time.sleep(1)
    # Check if the car can be added to hand
    can_add = check_add_to_hand()
    is_fusing = check_is_fusing()
    is_servicing = check_is_servicing()
    if can_add and not is_fusing and not is_servicing:
        tap_add_to_hand()
        time.sleep(1)
        return True
    else:
        tap_exit_car()
        time.sleep(1)
        return False


def add_from_garage(stop_event, number_of_cars: int, start_spot: int = 0) -> bool:
    """
    Adds cars from the garage to available slots.

    Args:
        number_of_cars (int): The number of cars to add to the hand.
        tries (int, optional): The number of tries to find and add a car. Defaults to 1.

    Returns:
        bool: True if cars are successfully added, False if there are not enough missing slots or an error occurs.
    """
    if stop_event.is_set():
        return False 
    # Check initial missing slots
    missing_slots = check_missing_slots()
    missing_slots_count = len(missing_slots)

    # If there are fewer missing slots than needed, return False (can't fill more than available)
    if number_of_cars > missing_slots_count:
        return False

    cars_added = 0

    while cars_added < number_of_cars:
        if stop_event.is_set():
            return False
        time.sleep(0.5)
        # Try to add car from the garage to the hand
        if add_car_to_hand(start_spot):
            cars_added += 1
        start_spot += 1

    # Check if we still have missing slots after adding the cars
    remaining_missing_slots = check_missing_slots()

    if missing_slots_count == len(remaining_missing_slots) + number_of_cars:
        return True
    else:
        if missing_slots_count < len(remaining_missing_slots) + number_of_cars:
            for _ in range(
                len(remaining_missing_slots) + number_of_cars - missing_slots_count
            ):
                while not add_car_to_hand(start_spot):
                    start_spot += 1
            if missing_slots_count == len(remaining_missing_slots) + number_of_cars:
                return True
            else:
                return False
        else:
            return False
