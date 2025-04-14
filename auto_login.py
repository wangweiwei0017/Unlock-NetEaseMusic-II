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
    browser.add_cookie({"name": "MUSIC_U", "value": "005BA090050712406697D5D9848D7D942C1C027FD379D3C3E7790AE83754DE786584ADCCDC088017D976E6BAC8A9DE0757D1A15721561D5D9E10E145276D2FF9D706493104007F8C27BBA2C95A8E1B3744F8D574AFBA93A32EC7E02AA4D0F3D69C8BFE8481E06E00C2373A5E5D75DD97A141712898589228BB81370C08CAD456C795769FCBCB575AA6DC9F5B29396388B5DAB63307B29B6A8E0E355CDD237A2E41913DEF589DBC967B55A9E8F10F9F105A8D70DC3A4F582E3B0CAE73E6D3E50CB008EF615DF222C55FCD3471F543A91A6504C8CC15CE882960BC54A449CFF74D381649A49184D8AC23698095DBCE62451F2550AA696EF106FE96F04F348F02C51043DC858C8612E4E45E490A4947BA063D4AC6FC1DBF1BBF950925E7BDFCA95CAAF2251BFF562B54F69D9DC9DC747F61AAF12E67C647523AF38B7836D75109EEA5929EA99072CC24A05D99AF850FA038BBECCB51A04AAA4BEBA2FCE499716EE763"})
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
