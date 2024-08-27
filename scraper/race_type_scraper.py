import os
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
from dotenv import load_dotenv
load_dotenv()

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode (no GUI)
chrome_options.add_argument("--disable-gpu")

# Path to your ChromeDriver
chrome_driver_path = os.getenv('CHROME_DRIVER_PATH')  # Replace with the path to your ChromeDriver

# Set up WebDriver
service = Service(chrome_driver_path)
print("service opened")
driver = webdriver.Chrome(service=service, options=chrome_options)
print("driver opened")
try:
    print("try to open website")
    time.sleep(2)
    # Open the website
    driver.get("https://www.topdrivesrecords.com/compare")  # Replace with your URL

    # Wait for the button to be clickable and click it
    wait = WebDriverWait(driver, 10)
    button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.D_Button.Main_AddTrackDirect.Main_AddTrackDirectLarger')))
    button.click()

    # Wait for the content to load after clicking the button
    time.sleep(5)  # Adjust this if needed based on the time required to load the content

    # Parse the updated page source with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Create a set to store unique track names
    track_names = set()

    # Find all elements with the class "Main_CustomTrackItem"
    custom_track_items = soup.find_all(class_='Main_CustomTrackItem')

    for item in custom_track_items:
        # Find the track name within each "Main_CustomTrackItem"
        track_name_div = item.find(class_='Main_CustomTrackName')
        if track_name_div:
            # Extract and clean the track name
            track_name = track_name_div.get_text(strip=True)
            # Remove unnecessary tags or characters
            track_name = track_name.split('<')[0].strip()  # Remove any HTML comments or extra tags
            track_names.add(track_name)

    # Output unique track names
    print("Unique Track Names:")
    # Save the set of track names to a CSV file
    with open('track_names.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        for name in sorted(track_names):
            writer.writerow([name.upper()])
            print(name)

finally:
    # Clean up and close WebDriver
    driver.quit()
