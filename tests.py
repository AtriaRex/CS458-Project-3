from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pyperclip


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

def test_1_correct_username_empty_password():
    driver = webdriver.Chrome()
    driver.get("http://127.0.0.1:5000")
    username = driver.find_element(By.ID, "email_phone")
    username.clear()
    username.send_keys("user1")

    password = driver.find_element(By.ID, "password")
    password.clear()
    username.send_keys(Keys.RETURN)

    assert "Logged in" not in driver.page_source
    assert "Wrong username or password" in driver.page_source
    driver.close()

    
def test_1_empty_username_correct_password():
    driver = webdriver.Chrome()
    driver.get("http://127.0.0.1:5000")
    username = driver.find_element(By.ID, "email_phone")
    username.clear()

    password = driver.find_element(By.ID, "password")
    password.clear()
    password.send_keys("pass1")
    username.send_keys(Keys.RETURN)

    assert "Logged in" not in driver.page_source
    assert "Wrong username or password" in driver.page_source
    driver.close()




def test_1_correct_username_incorrect_password():
    driver = webdriver.Chrome()
    driver.get("http://127.0.0.1:5000")
    username = driver.find_element(By.ID, "email_phone")
    username.clear()
    username.send_keys("user1")

    password = driver.find_element(By.ID, "password")
    password.clear()
    password.send_keys("incorrect")
    username.send_keys(Keys.RETURN)

    assert "Logged in" not in driver.page_source
    assert "Wrong username or password" in driver.page_source
    driver.close()


def test_1_incorrect_username_correct_password():
    driver = webdriver.Chrome()
    driver.get("http://127.0.0.1:5000")
    username = driver.find_element(By.ID, "email_phone")
    username.clear()
    username.send_keys("incorrect")

    password = driver.find_element(By.ID, "password")
    password.clear()
    password.send_keys("pass1")
    username.send_keys(Keys.RETURN)

    assert "Logged in" not in driver.page_source
    assert "Wrong username or password" in driver.page_source
    driver.close()

def test_3_sql_injection_in_username_field():
    driver = webdriver.Chrome()
    driver.get("http://127.0.0.1:5000")
    username = driver.find_element(By.ID, "email_phone")
    username.clear()
    username.send_keys("' OR '1'='1")

    password = driver.find_element(By.ID, "password")
    password.clear()
    password.send_keys("pass1")
    username.send_keys(Keys.RETURN)

    assert "Logged in" not in driver.page_source
    assert "Wrong username or password" in driver.page_source
    driver.close()


def test_3_sql_injection_in_password_field():
    driver = webdriver.Chrome()
    driver.get("http://127.0.0.1:5000")
    username = driver.find_element(By.ID, "email_phone")
    username.clear()
    username.send_keys("user1")

    password = driver.find_element(By.ID, "password")
    password.clear()
    password.send_keys("' OR '1'='1")
    username.send_keys(Keys.RETURN)

    assert "Logged in" not in driver.page_source
    assert "Wrong username or password" in driver.page_source
    driver.close()


def test_4_cant_paste_password():
    correct_password = "pass1"
    pyperclip.copy(correct_password)
    
    driver = webdriver.Chrome()
    driver.get("http://127.0.0.1:5000")
    username = driver.find_element(By.ID, "email_phone")
    username.clear()
    username.send_keys("user1")

    password = driver.find_element(By.ID, "password")
    password.clear()
    password.send_keys(Keys.CONTROL, "v")

    username.send_keys(Keys.RETURN)

    assert "Logged in" not in driver.page_source
    assert "Wrong username or password" in driver.page_source
    driver.close()



def main():
    test_1_correct_inputs_log_in()
    test_1_correct_username_incorrect_password()
    test_1_incorrect_username_correct_password()
    test_1_empty_username_correct_password()
    test_1_correct_username_empty_password()

    test_3_sql_injection_in_password_field()
    test_3_sql_injection_in_username_field()

    test_4_cant_paste_password()

    # if execution reached here without any errors then all test have passed
    print("All tests have passed")

main()
