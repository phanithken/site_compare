# coding=utf-8
import argparse
import os

# selenium
from io import BytesIO

from imageio.core import Image
from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from screenshot import Screenshot_Clipping

# logging
from logging import getLogger, StreamHandler, DEBUG
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
handler.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False

# parse arguments
# first argument should be first site
# second argument should be second site
# third argument should be path.txt, containing all path of the site
parser = argparse.ArgumentParser(description='comparision between two sites')
parser.add_argument('-p', '--arg1')
parser.add_argument('arg2', help='first site')
parser.add_argument('arg3', help='second site')
args = parser.parse_args()


def process():
    print('processing')
    print(args.arg1)
    print(args.arg2)
    print(args.arg3)


def take_screenshot():
    options = webdriver.ChromeOptions()

    # for mobile site
    mobile_emulation = { "deviceName": "iPhone X" }
    # options.add_experimental_option("mobileEmulation", mobile_emulation)
    options.headless = True

    ob = Screenshot_Clipping.Screenshot()
    driver = webdriver.Chrome(executable_path=os.path.join(os.getcwd(), 'chromedriver'), options=options)

    url = "https://sp.subaru.jp"

    driver.get(url)

    try:
        w = WebDriverWait(driver, 8)
        w.until(expected_conditions.presence_of_element_located((By.TAG_NAME, "body")))
        S = lambda X: driver.execute_script('return document.body.parentNode.scroll' + X)
        driver.set_window_size(S('Width'), S('Height'))  # may need manual adjustment
        img_url = ob.full_Screenshot(driver, save_path=r'.', image_name='google.png')
        print(img_url)
        # p = driver.get_window_size()
        # print(p['width'], p['height'])
        # driver.find_element_by_tag_name('body').screenshot('web_screenshot.png')
        # driver.save_screenshot('test.png')
    except TimeoutException:
        print("Timeout page load too long")

    # driver.close()

    driver.quit()


if __name__ == "__main__":
    take_screenshot()
    # print(os.path.join(os.getcwd(), 'chromedriver.exe'))
