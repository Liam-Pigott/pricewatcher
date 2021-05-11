import json
import os
import database
from sqlalchemy import select
from database import Watcher, Price
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from datetime import date, datetime
from types import SimpleNamespace

# Config

# Get the current porject path so we can schedule/run from anywhere
project_path = os.path.dirname(__file__)

with open(os.path.join(project_path, 'config/config.json'), 'r') as c:
    config = json.load(c)

# Constants
HEADLESS_DRIVER=config['use_headless_driver']

def main():
    print('Setting up database and session')
    session = database.setup_db_session()
    print('DB and session setup complete')

    driver = setup_driver()
    watchers = session.query(Watcher).all()
    prices = check_prices_for_watchers(driver, watchers)
    database.commit_prices(prices, session)
    

def check_prices_for_watchers(driver, watchers):
    prices = []
    for watcher in watchers:
        driver.get(watcher.url)
        price = get_element_by_xpath(driver, watcher.xpath)
        if price:
            price = float(format_price(price.text))
            price_object = Price(watcher_id=watcher.id, price=price, date_time=datetime.now())
            prices.append(price_object)
        else:
            print("Couldn't find price object for product: [{}{}]".format(watcher.name, watcher.url))
    return prices

# surrounding in try catch when we need to call from multiple places
def get_element_by_xpath(driver, xpath):
    try:
        return driver.find_element_by_xpath(xpath)
    except NoSuchElementException as err:
        print(err.msg)

# Helper functions 
def format_price(price):
    return price.strip('£')

def setup_driver():
    options = Options()
    if HEADLESS_DRIVER:
        options.headless = True
        options.add_argument("--window-size=1920,1200")

    driver = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install(), options=options)
    return driver

if __name__ == "__main__":
    main()