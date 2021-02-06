import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

#Config
with open('config/config.json', 'r') as c:
    config = json.load(c)

with open('config/watchers.json', 'r') as w:
    watchers = json.load(w)

# Constants
DRIVER_PATH=config['driver_path']

# Main Loop
def main():
    driver = setup_driver()
    get_and_print(driver, watchers)
    driver.quit()


def get_and_print(driver, watchers):
    for watch in watchers:
        driver.get(watch.get("url"))
        price = driver.find_element_by_xpath(watch.get("xpath"))
        if price:
            price = float(format_price(price.text))
        print(watch.get("name") + "\n" + watch.get("url") + "\n" + str(price))

# Helper functions 
def format_price(price):
    return price.strip('£')

def setup_driver():
    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1200")

    driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
    return driver

if __name__ == "__main__":
    main()



