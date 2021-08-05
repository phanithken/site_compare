from selenium import webdriver

options = webdriver.ChromeOptions()
# mobile_emulation = {"deviceName": "iPhone X"}
options.headless = True
options.add_argument('--ignore-certificate-errors')
# options.add_argument("--test-type")
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

try:
    chromedriver_path = "/usr/bin/chromedriver"
    with webdriver.Chrome(executable_path=chromedriver_path, options=options) as driver:
        driver.get("https://www.google.com")
        driver.quit()
except Exception as e:
    print(e)
    pass