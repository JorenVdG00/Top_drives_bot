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