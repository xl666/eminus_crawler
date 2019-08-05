from selenium import webdriver
import sys

salida = sys.stdout
MAX_PROCESS = 10 # Para el pull de procesos, no se recomienda más grande


def configure():
    options = webdriver.ChromeOptions()
    #options.binary_location = '/usr/bin/chromium'
    options.add_argument('headless')
    options.add_argument('window-size=1800x1024')
    options.add_argument("--log-level=3");
    options.add_argument("--silent");
    driver = webdriver.Chrome(options=options)
    return driver
