from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By



def test_1_correct_inputs_log_in():
    driver = webdriver.Chrome()
    driver.get("http://127.0.0.1:5000")
    username = driver.find_element(By.ID, "email_phone")
    username.clear()
    username.send_keys("user1")

    password = driver.find_element(By.ID, "password")
    password.clear()
    password.send_keys("pass1")
    username.send_keys(Keys.RETURN)


    assert "Logged in" in driver.page_source
    assert "username or password is wrong." not in driver.page_source
    driver.close()



test_1_correct_inputs_log_in()