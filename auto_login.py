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
    browser.add_cookie({"name": "MUSIC_U", "value": "007DA361A6276F29D106E5CC46068BA13E7984B26153F902410656C288972BD5BC26DAFD3481D723CB1999AE6606BF634C26EA9302271C345DFC79E4F106A1358D83681177B0D64FAEABEED2C4018718C13F3F8341CA1CBC420949CF8FECBB115F8612275344726406F96893E1C2D0CCA52A5BF6EF75E24B7D9B4DB278DF825F232358793A87ED3484E431D87AA40CD987B65656BCC4093C23DCA4427851BB1C83CAAC4F1F67543DA2753FE79F64A247D98E906B120C6A49C32110E02AF28821FD0200E11858756BD75F98107950B20CF6C2D608F2E68CCF758F4B8E24688DEC3F664CD60DBF1CDFA2B18A4E0E2FB66A85A28601EADF9D0CB717195B4E7498795FEB9DFCAF6A9165A2CCEABE1AE1B32590891EEF55B9CA85557E7E96070C29D53A6461876D001EC10D7B61ABA76C5FBC0C743F3743D798CACD7D62121C0BA1FA0C2509623975959F8BBB90D9F537D3976A6D2C6C5DCA2DD1B9694AFFA5736D77A7"})
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
