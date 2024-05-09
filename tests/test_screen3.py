
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

from src.routes import calculate_distance_to_sun_helper

load_dotenv()

def selenium_set_up():
    driver = webdriver.Chrome()
    
    if os.environ.get("CHROME_USER_DATA_DIR") != None and os.environ.get("CHROME_USER_DATA_DIR") != "":
        print(os.environ.get("CHROME_USER_DATA_DIR"))
        
        options = webdriver.ChromeOptions() 
        options.add_argument("user-data-dir=" + os.environ["CHROME_USER_DATA_DIR"])
        service = Service(executable_path=os.environ["CHROME_EXE_PATH"])
        driver = webdriver.Chrome(service=service, options=options)

    driver.execute_script(
        f"""
  window.navigator.geolocation.getCurrentPosition = function(success) {{
    var position = {{
      "coords": {{
        "latitude": "39",
        "longitude": "36"
      }}
    }};
    success(position);
  }};
"""
    )
    
    driver.get("http://127.0.0.1:5000")
    username = driver.find_element(By.ID, "email_phone")
    username.clear()
    password = driver.find_element(By.ID, "password")
    password.clear()

    username.send_keys("admin@admin.com")
    password.send_keys("admin123")

    username.send_keys(Keys.RETURN)

    driver.find_element(By.ID, "sun-calculation").click()

    return driver
    
def test_january_closer_than_july():
    january_distance = calculate_distance_to_sun_helper(0,0, Time("2022-01-01"))
    july_distance = calculate_distance_to_sun_helper(0,0, Time("2022-07-01"))

    assert january_distance < july_distance

def test_sun_calculation_within_limits():
    for i in range(5):
        longitude = random.random() * 360 - 180
        latitude = random.random() * 180 - 90
        distance = calculate_distance_to_sun_helper(longitude, latitude, Time("2022-01-01"))
        assert distance > 146000000 # 146 million km
        assert distance < 153000000 # 153 million km

def test_only_numbers_allowed_in_coordinate_field():
    driver = selenium_set_up()

    lon_type = driver.find_element(By.ID, "longitude").get_dom_attribute("type")
    lat_type = driver.find_element(By.ID, "latitude").get_dom_attribute("type")

    assert lon_type == "number"
    assert lat_type == "number"

    driver.close()

def test_invalid_input_not_allowed():
    driver = selenium_set_up()

    longitude = driver.find_element(By.ID, "longitude")
    latitude = driver.find_element(By.ID, "latitude")
    submit_button = driver.find_element(By.ID, "manualCalculation")

    longitude.clear()
    latitude.send_keys("30asd")

    assert latitude.get_attribute("value") == "30"

    driver.close()

def test_submit_button_disabled_when_both_fields_empty():
    driver = selenium_set_up()

    submit_button = driver.find_element(By.ID, "manualCalculation")
    assert submit_button.get_dom_attribute("disabled") == "true"

    driver.close()

def test_submit_button_disabled_when_one_field_empty():
    driver = selenium_set_up()

    longitude = driver.find_element(By.ID, "longitude")
    latitude = driver.find_element(By.ID, "latitude")
    submit_button = driver.find_element(By.ID, "manualCalculation")

    longitude.send_keys("30")
    assert submit_button.get_dom_attribute("disabled") == "true"

    longitude.clear()
    latitude.send_keys("30")
    assert submit_button.get_dom_attribute("disabled") == "true"

    driver.close()

def test_sql_injection_on_coordinates():
    driver = selenium_set_up()

    longitude = driver.find_element(By.ID, "longitude")
    latitude = driver.find_element(By.ID, "latitude")

    longitude.send_keys("' OR '1'='1")
    latitude.send_keys("30")

    assert longitude.get_attribute("value") == "11"