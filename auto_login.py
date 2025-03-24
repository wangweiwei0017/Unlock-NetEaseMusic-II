# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "00E43536BBB4866A14766FB3E510A928F51E6B428A342765E260053D4402F986AA886BB453ABA91FB5FF2B9BD3DF603C99FFF7B78D130BBDEAD062A4C8C1D74C88B397ADC11B60F0343B884FD9B8508703402309610B67C6090E3699E3219DE4BFE3B7443887586CCFD28D1A78F82030F96B0883918AA80E8D7D7987E2943DE20EE5678F1068016D5F54380ADAC3F2C4C175801C11289D783325A04FF4BE935BF3A29A8348E380B2A2AD597368C1484DBB7A2D423972ECA5E59EADE8C862FDD93D76693941E789BD3CA0E87AE1751D022843DCB3703DE75567AEB125C50927E70DA28D02B43E5CDCF9062B05900E0ED445182B2AD86C170B1E54BA78B044B48C1B63FD1A1245C3CC2EA55123BD2EA2B547E5EECBE15D267A784A4C6A1F6DC1D99DB4C7F5C7FC2A31DBE6D1E83F9DEAF8F4A969B297279F1AD107358DE4D3CAC3749F4169A3C8732C090B886DC78EC1322DD3F8FFCDF5CCDB0ABC4331BB1F88ACC7"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
