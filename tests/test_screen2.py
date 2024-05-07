from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import pyperclip
from dotenv import load_dotenv
import os
import random
from astropy.time import Time

from src.routes import calculate_distance_to_sun_helper, get_closest_sea_helper

load_dotenv()

def selenium_set_up():
    driver = webdriver.Chrome()
    
    if os.environ.get("CHROME_USER_DATA_DIR") != None and os.environ.get("CHROME_USER_DATA_DIR") != "":
        print(os.environ.get("CHROME_USER_DATA_DIR"))
        
        options = webdriver.ChromeOptions() 
        options.add_argument("user-data-dir=" + os.environ["CHROME_USER_DATA_DIR"])
        service = Service(executable_path=os.environ["CHROME_EXE_PATH"])
        driver = webdriver.Chrome(service=service, options=options)
    
    driver.get("http://127.0.0.1:5000")
    username = driver.find_element(By.ID, "email_phone")
    username.clear()
    password = driver.find_element(By.ID, "password")
    password.clear()

    username.send_keys("admin@admin.com")
    password.send_keys("admin123")

    username.send_keys(Keys.RETURN)

    assert LOGGED_IN_MSG in driver.page_source
    assert WRONG_CREDENTIALS_MSG not in driver.page_source


    return driver

def test_distance_in_meters():
    driver = selenium_set_up()

    text = driver.find_element(By.ID, "distanceToNearestSeaText").get_attribute("value")
    assert "kilometers" not in text
    assert "meters" in text


def test_should_not_return_lakes():
    sea = get_closest_sea_helper(39.40, 38.48) # coordinates of Hazar Lake in Turkey
    assert sea["sea"] != "Hazar Lake"

    sea = get_closest_sea_helper(42.91, 38.61) # coordinates of Van Lake in Turkey
    assert sea["sea"] != "Van Lake"

def test_maximum_distance():
    for i in range(5):
        longitude = random.random() * 9 + 26 # longitude in Turkey
        latitude = random.random() * 6 + 36 # latitude in Turkey
        sea = get_closest_sea_helper(longitude, latitude)
        assert sea["distance"] < 1650000 # 1650 km

def test_correct_sea_returned():
    sea = get_closest_sea_helper(39.71, 41.00) # coordinates of Trabzon 
    assert sea["sea"] == "Black Sea"

    sea = get_closest_sea_helper(30.70, 36.39) # coordinates of Antalya
    assert sea["sea"] == "Mediterranean Sea"

    sea = get_closest_sea_helper(27.14, 38.42) # coordinates of Izmir
    assert sea["sea"] == "Aegean Sea"

