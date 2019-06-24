from selenium import webdriver
import sys

salida = sys.stdout

def configure():
    options = webdriver.ChromeOptions()
    options.binary_location = '/usr/bin/chromium'
    options.add_argument('headless')
    options.add_argument('window-size=1800x1024')
    driver = webdriver.Chrome(chrome_options=options)
    return driver
