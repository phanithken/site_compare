from selenium import webdriver
from PIL import Image
from io import BytesIO
import time
import os
import argparse
import shutil


# parse arguments
# first argument should be first site
# second argument should be second site
# third argument should be path.txt, containing all path of the site
parser = argparse.ArgumentParser(description='comparision between two sites')
parser.add_argument('-p', '--arg1')
parser.add_argument('arg2', help='first site')
parser.add_argument('arg3', help='second site')
args = parser.parse_args()


def fullpage_screenshot(driver, file, scroll_delay=0.3):
    device_pixel_ratio = driver.execute_script('return window.devicePixelRatio')

    total_height = driver.execute_script('return document.body.parentNode.scrollHeight')
    viewport_height = driver.execute_script('return window.innerHeight')
    total_width = driver.execute_script('return document.body.offsetWidth')
    viewport_width = driver.execute_script("return document.body.clientWidth")

    assert(viewport_width == total_width)

    # scroll the page, take screenshots and save screenshots to slices
    offset = 0
    slices = {}
    while offset < total_height:
        if offset + viewport_height > total_height:
            offset = total_height - viewport_height

        driver.execute_script('window.scrollTo({0}, {1})'.format(0, offset))
        time.sleep(scroll_delay)

        img = Image.open(BytesIO(driver.get_screenshot_as_png()))
        slices[offset] = img

        offset = offset + viewport_height

    # combine image slices
    stitched_image = Image.new('RGB', (total_width * device_pixel_ratio, total_height * device_pixel_ratio))
    for offset, image in slices.items():
        stitched_image.paste(image, (0, offset * device_pixel_ratio))
    stitched_image.save(file)


def get_screenshot_from_url(URL, FILENAME):
    options = webdriver.ChromeOptions()
    mobile_emulation = {"deviceName": "iPhone X"}
    options.headless = True
    options.add_experimental_option("mobileEmulation", mobile_emulation)
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--test-type")
    with webdriver.Chrome(executable_path=os.path.join(os.getcwd(), 'chromedriver'), options=options) as driver:
        print("Processing screenshot: " + URL)
        driver.get(URL)
        fullpage_screenshot(driver, FILENAME)
        driver.quit()


def process():
    # read path file
    path = args.arg1
    site1 = args.arg2
    site2 = args.arg3

    output = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
    site1dir = os.path.join(output, site1)
    site2dir = os.path.join(output, site2)

    # delete old data
    shutil.rmtree(site1dir)
    shutil.rmtree(site2dir)

    # create output directory
    os.makedirs(site1dir)
    os.makedirs(site2dir)

    lines = tuple(open(path, "r"))

    for x in lines:
        desire_path = x.replace("\n", "")
        filename = desire_path.replace("/", "_") + ".png"

        get_screenshot_from_url("https://" + site1 + desire_path, os.path.join(site1dir, filename))
        get_screenshot_from_url("https://" + site2 + desire_path, os.path.join(site2dir, filename))


if __name__ == '__main__':
    # get_screenshot_from_url('https://sp.subaru.jp.internal', 'screenshot1.png')
    process()