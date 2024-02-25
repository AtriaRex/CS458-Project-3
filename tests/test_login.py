from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pyperclip

LOGGED_IN_MSG = "You are logged in"
INVALID_EMAIL_OR_PHONE_MSG = "Please enter a valid Email Address or a Phone Number"
WRONG_CREDENTIALS_MSG = "Incorrect Email Address/Phone Number or Password"
INPUT_CANT_BE_BLANK_MSG = "Email Address/Phone Number or Password cannot be blank"

def set_up():
    driver = webdriver.Chrome()
    driver.get("http://127.0.0.1:5000")
    username = driver.find_element(By.ID, "email_phone")
    username.clear()
    password = driver.find_element(By.ID, "password")
    password.clear()

    return (driver, username, password)
    
def test_1_correct_inputs_log_in():
    (driver, username, password) = set_up()
    username.send_keys("admin@admin.com")
    password.send_keys("admin123")

    username.send_keys(Keys.RETURN)

    assert LOGGED_IN_MSG in driver.page_source
    assert WRONG_CREDENTIALS_MSG not in driver.page_source
    driver.close()

def test_1_correct_username_empty_password():
    (driver, username, password) = set_up()
    username.send_keys("admin@admin.com")
    username.send_keys(Keys.RETURN)

    assert LOGGED_IN_MSG not in driver.page_source
    assert INPUT_CANT_BE_BLANK_MSG in driver.page_source
    driver.close()

    
def test_1_empty_username_correct_password():
    (driver, username, password) = set_up()

    password.send_keys("admin123")
    username.send_keys(Keys.RETURN)

    assert LOGGED_IN_MSG not in driver.page_source
    assert INPUT_CANT_BE_BLANK_MSG in driver.page_source
    driver.close()

def test_1_correct_username_incorrect_password():
    (driver, username, password) = set_up()
    username.send_keys("admin@admin.com")

    password.send_keys("incorrect")
    username.send_keys(Keys.RETURN)

    assert LOGGED_IN_MSG not in driver.page_source
    assert WRONG_CREDENTIALS_MSG in driver.page_source
    driver.close()

def test_1_incorrect_username_correct_password():
    (driver, username, password) = set_up()
    username.send_keys("notadmin@admin.com")

    password.send_keys("admin123")
    username.send_keys(Keys.RETURN)

    assert LOGGED_IN_MSG not in driver.page_source
    assert WRONG_CREDENTIALS_MSG in driver.page_source
    driver.close()

def test_3_sql_injection_in_username_field():
    (driver, username, password) = set_up()
    username.send_keys("' OR '1'='1")

    password.send_keys("admin123")
    username.send_keys(Keys.RETURN)

    assert LOGGED_IN_MSG not in driver.page_source
    assert INVALID_EMAIL_OR_PHONE_MSG in driver.page_source
    driver.close()


def test_3_sql_injection_in_password_field():
    (driver, username, password) = set_up()
    username.send_keys("admin@admin.com")

    password.send_keys("' OR '1'='1")
    username.send_keys(Keys.RETURN)

    assert LOGGED_IN_MSG not in driver.page_source
    assert WRONG_CREDENTIALS_MSG in driver.page_source
    driver.close()


def test_4_password_field_not_pastable():
    (driver, username, password) = set_up()
    correct_password = "admin123"
    pyperclip.copy(correct_password)
    
    username.send_keys("admin@admin.com")

    password.send_keys(Keys.CONTROL, "v")
    username.send_keys(Keys.RETURN)

    assert LOGGED_IN_MSG not in driver.page_source
    assert INPUT_CANT_BE_BLANK_MSG in driver.page_source
    driver.close()

def test_5_signin_out_clears_credentials():
    (driver, username, password) = set_up()
    username.send_keys("admin@admin.com")
    password.send_keys("admin123")
    username.send_keys(Keys.RETURN)

    logout_button = driver.find_element(By.ID, "logout")
    logout_button.click()

    # check that the username and password are empty
    username = driver.find_element(By.ID, "email_phone").get_attribute("value")
    password = driver.find_element(By.ID, "password").get_attribute("value")

    assert username == ""
    assert password == ""
    
