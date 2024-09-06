import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from database.methods.db_adder import add_club_reqs, add_track_set, add_race, add_club_track_set, add_track_serie
from database.methods.db_delete import delete_club_track_sets,delete_club_reqs
from bs4 import BeautifulSoup
import time

# Path to your ChromeDriver
chrome_driver_path = os.getenv('CHROME_DRIVER_PATH')  # Replace with the path to your ChromeDriver

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode (no GUI)
chrome_options.add_argument("--disable-gpu")

# Set up WebDriver
service = Service(chrome_driver_path)
print("service opened")
driver = webdriver.Chrome(service=service, options=chrome_options)
print("driver opened")

# Wait for the page to load (adjust if necessary)
driver.implicitly_wait(10)  # waits up to 10 seconds
driver.get("https://www.topdrivesrecords.com/clubs")

wait = WebDriverWait(driver, 10)


def get_track_names():
    track_names = []
    # Find all buttons within the first Clubs_SelectorBox (for track names)
    track_buttons = driver.find_elements(By.CSS_SELECTOR,
                                         "div.Clubs_Box > div.Clubs_SelectorBox:first-of-type button span.BaseChip_Text")

    # Extract and print the track names
    print("Track Names:")
    for button in track_buttons:
        print(button.text)
        track_names.append(button.text)
    return track_names

def fix_conditions(condition_spans):
    conditions = []
    for span in condition_spans:
        condition_type = span.text.strip()
        if condition_type.upper() == 'ASPHT':
            condition_type = 'ASPHALT'
        elif condition_type.upper() == 'WET':
            condition_type = 'WET'
        elif condition_type.upper() == 'DIRT':
            condition_type = 'DIRT'
        else:
            condition_type = condition_type.upper()
        conditions.append(condition_type)
    return conditions


def check_icon(track, conditions):
    # Check SVG icon for additional conditions
    icon_layout = track.find('div', class_='BaseIconSvg_Layout')
    if icon_layout:
        svg = icon_layout.find('svg')
        if svg:
            if 'BaseIconSvg_Roll' in svg.get('class', []):
                conditions.append('ROLLING')
            elif 'BaseIconSvg_Clearance' in svg.get('class', []):
                conditions.append('HIGH')
    return conditions
def get_race_tracks():
    race_tracks = {}
    track_buttons = wait.until(EC.presence_of_all_elements_located(
        (By.CSS_SELECTOR, "div.Clubs_Box > div.Clubs_SelectorBox:nth-of-type(1) button span.BaseChip_Text")))

    # Click on each track and get the information
    for index, button in enumerate(track_buttons):
        club_event_name = button.text
        cleaned_club_event_name = club_event_name.upper().replace(' ', '_').strip()
        print(cleaned_club_event_name)
        print(f"Clicking on track {index + 1}: {button.text}")
        track_button = button.find_element(By.XPATH, '..')  # Find the parent button element
        track_button.click()
        time.sleep(2)
        # Get the page source after interacting with the page
        html_content = driver.page_source

        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        track_boxes = soup.find_all('div', class_='Cg_Box BaseEventTrackbox_BoxRelative')
        count = 1
        track_set_id = add_track_set()
        for track_box in track_boxes:
            track_serie = add_track_serie(track_set_id)
            print(count)
            count += 1
            race_number = 1
            tracks = track_box.find_all('div', class_='Cg_Track EventTrack')
            for track in tracks:
                content = track.find('div', class_='Row_Content').text.strip().upper()
                # Extract conditions
                conditions_div = track.find('div', class_='Row_Conditions')
                conditions = []

                if conditions_div:
                    base_type_layout = conditions_div.find('div', class_='BaseTypeName_Layout')
                    if base_type_layout:
                        spans = base_type_layout.find_all('span')
                        conditions = fix_conditions(spans)

                conditions = check_icon(track, conditions)
                conditions_dict = {'WET': False,
                                   'SUN': False,
                                   'HIGH': False,
                                   'ROLLING': False}
                road_types = []
                if 'WET' in conditions:
                    conditions_dict['WET'] = True
                    conditions_dict['SUN'] = False
                else:
                    conditions_dict['WET'] = False
                    conditions_dict['SUN'] = True

                if 'HIGH' in conditions:
                    conditions_dict['HIGH'] = True
                if 'ROLLING' in conditions:
                    conditions_dict['ROLLING'] = True

                for condition in conditions:
                    if condition not in conditions_dict:
                        road_types.append(condition)

                if len(road_types) > 1:
                    road_type = 'MIXED'
                elif len(road_types) == 1:
                    road_type = road_types[0]
                elif not road_types:
                    road_type = 'ASPHALT'


                print(f'Content: {content}')
                print(f'Conditions: {conditions_dict}')
                print(f'Road type: {road_type}')
                print('---'*5)
                add_race(content, road_type, conditions_dict, race_number, track_serie)
        add_club_track_set(cleaned_club_event_name, track_set_id)
def get_club_req_list():
    # Find all buttons within the second Clubs_SelectorBox (for requirements)
    requirement_buttons = driver.find_elements(By.CSS_SELECTOR,
                                               "div.Clubs_Box > div.Clubs_SelectorBox:nth-of-type(2) button span.BaseChip_Text")

    # Extract and print the requirements
    print("\nRequirements:")
    req_list = []
    for button in requirement_buttons:
        text = button.text
        print("Original text:", text)

        # Split by comma to handle multiple requirements
        req_split = text.split(",")
        print('req_split =', req_split)

        req_dict = {}
        for req in req_split:
            # Strip any extra spaces and split by space
            split_req = req.strip().split(" ")

            # Handle cases where there might be multiple spaces
            if len(split_req) >= 2:
                amount_str = split_req[0]
                type_str = " ".join(split_req[1:])  # Join the rest of the split parts to get the full type string

                # Remove 'x' from amount_str
                amount = amount_str.replace('x', "").strip()

                # Add to dictionary
                req_dict[type_str] = amount

        # Append the dictionary to the list
        req_list.append(req_dict)
    return req_list


def add_club_req_db(req_list):
    for req_dict in req_list:
        type = []
        amount = []
        for key, value in req_dict.items():
            type.append(key)
            amount.append(value)
        if len(type) == 2:
            add_club_reqs(type[0], amount[0], type[1], amount[1])
        elif len(type) == 1:
            add_club_reqs(type[0], amount[0], None, None)
        else:
            add_club_reqs(None, None, None, None)


def refresh_club_info():
    delete_club_track_sets()
    delete_club_reqs()
    add_club_req_db(get_club_req_list())
    get_race_tracks()



refresh_club_info()

# Close the Selenium WebDriver
driver.quit()
