from selenium import webdriver
from PIL import Image
from io import BytesIO
from skimage.metrics import structural_similarity
from logging import getLogger, StreamHandler, DEBUG
from utils import append_to_file

import cv2
import time
import os
import sys
import argparse
import shutil

# logging
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
parser.add_argument('-s', '--smartphone', action='store_true', help='smartphone mode')
parser.add_argument('arg2', help='first site')
parser.add_argument('arg3', help='second site')
args = parser.parse_args()


def fullpage_screenshot(driver, file, scroll_delay=0.3):
    device_pixel_ratio = driver.execute_script('return window.devicePixelRatio')

    total_height = driver.execute_script('return document.body.parentNode.scrollHeight')
    viewport_height = driver.execute_script('return window.innerHeight')
    total_width = driver.execute_script('return document.body.offsetWidth')
    viewport_width = driver.execute_script("return document.body.clientWidth")

    # assert(viewport_width == total_width)
    if (viewport_width != total_width):
        return False

    # TO-DO: handle assert error, in case of 404 or anything sort of that

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
    return True


def get_screenshot_from_url(URL, FILENAME):
    options = webdriver.ChromeOptions()
    mobile_emulation = {"deviceName": "iPhone X"}
    options.headless = True
    if args.smartphone:
        options.add_experimental_option("mobileEmulation", mobile_emulation)
        options.add_argument('window-size=375,812')
    else:
        options.add_argument('window-size=1920,1080')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--test-type")
    with webdriver.Chrome(executable_path=os.path.join(os.getcwd(), 'chromedriver'), options=options) as driver:
        print("Processing screenshot: " + URL)
        driver.get(URL)
        if "404" not in driver.title:
            return fullpage_screenshot(driver, FILENAME)
        else:
            print("Not Found: " + URL)
            return False
        driver.quit()


# take two image as input and output the result including red rectangle
def compare_image(img1, img2):
    image1 = cv2.imread(img1, 1)
    image2 = cv2.imread(img2, 1)

    height1, width1 = image1.shape[:2]
    height2, width2 = image2.shape[:2]

    height = min(height1, height2)
    width = min(width1, width2)

    # change to gray scale & align height/width
    gray1 = cv2.cvtColor(image1[0:height, 0:width], cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(image2[0:height, 0:width], cv2.COLOR_BGR2GRAY)

    try:
        # compare image
        (score, diff) = structural_similarity(gray1, gray2, full=True, multichannel=True)
        diff = (diff * 255).astype("uint8")

    except ValueError as e:
        logger.debug("ValueError: ({0})".format(e))
        return 0
    except:
        logger.debug("Unexpected error: " + str(sys.exc_info()[0]))
        return 0

    # mark differences
    threshold = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    cnts = cv2.findContours(threshold.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0]

    for c in cnts:
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(image1, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.rectangle(image2, (x, y), (x + w, y + h), (0, 0, 255), 2)

    if score < 0:
        percent = ((score * 100) / 2) - 50
        logger.debug(img1 + ', ' + img2 + ', ' + "Similarity: {0}%".format(percent))

    else:
        percent = round(((score * 100) / 2) + 50, 2)
        logger.debug(img1 + ', ' + img2 + ', ' + "Similarity: {0}%".format(percent))

    # create output dir in both site folder
    if not os.path.exists(os.path.join(os.path.dirname(img1), "output")): os.makedirs(os.path.join(os.path.dirname(img1), "output"))
    if not os.path.exists(os.path.join(os.path.dirname(img2), "output")): os.makedirs(os.path.join(os.path.dirname(img2), "output"))

    # write output to dir
    cv2.imwrite(os.path.join(os.path.join(os.path.dirname(img1), "output"), os.path.basename(img1)), image1)
    cv2.imwrite(os.path.join(os.path.join(os.path.dirname(img2), "output"), os.path.basename(img2)), image2)
    cv2.waitKey(0)

    path1 = os.path.splitext(os.path.basename(img1))[0].replace("_", "/")
    path2 = os.path.splitext(os.path.basename(img2))[0].replace("_", "/")

    # TO-DO: normalize
    return "https://" + args.arg2 + path1 + ', ' "https://" + args.arg3 + path2 + ', ' + "Similarity: {0}%".format(percent)

def process():
    # read path file
    path = args.arg1
    site1 = args.arg2
    site2 = args.arg3

    output = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
    site1dir = os.path.join(output, site1)
    site2dir = os.path.join(output, site2)

    # delete old data
    if os.path.exists(site1dir): shutil.rmtree(site1dir)
    if os.path.exists(site2dir): shutil.rmtree(site2dir)

    # create output directory
    os.makedirs(site1dir)
    os.makedirs(site2dir)

    lines = tuple(open(path, "r"))

    for x in lines:
        desire_path = x.replace("\n", "")
        filename = desire_path.replace("/", "_") + ".png"

        # prepare screenshot for each path of the site
        is_site1_screenshot = get_screenshot_from_url("https://" + site1 + desire_path, os.path.join(site1dir, filename))
        is_site2_screenshot = get_screenshot_from_url("https://" + site2 + desire_path, os.path.join(site2dir, filename))

        if (is_site1_screenshot and is_site2_screenshot):
            # generate comparision of the screenshot
            msg = compare_image(os.path.join(site1dir, filename), os.path.join(site2dir, filename))

            # add similarity to result
            result = os.path.basename("result.txt")
            if not os.path.exists(result): open(result, "w")
            append_to_file(result, msg)
            print(msg)
        else:
            err = os.path.basename("error.txt")
            if not is_site1_screenshot:
                msg = "https://" + site1 + desire_path
                print("error at: " + msg)
                append_to_file(err, msg)

            if not is_site2_screenshot:
                msg = "https://" + site2 + desire_path
                print("error at: " + msg)
                append_to_file(err, msg)
                print()


if __name__ == '__main__':
    process()