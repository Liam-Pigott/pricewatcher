#!/usr/bin/python
import json
import database
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

# Config

# Get the current porject path so we can schedule/run from anywhere
project_path = os.path.dirname(__file__)

with open(os.path.join(project_path, 'config/config.json'), 'r') as c:
    config = json.load(c)

with open(os.path.join(project_path, 'config/products.json'), 'r') as w:
    products = json.load(w)

# Constants
DRIVER_PATH=config['driver_path']
IS_SAVE_DB=config['is_include_database']
HEADLESS_DRIVER=config['use_headless_driver']

def main():
    driver = setup_driver()
    conn = None
    # Allows control of print vs store in db
    if IS_SAVE_DB:
        conn = database.connect()
        cursor = conn.cursor()
        # Assumes database exists, creates table if not exists
        database.create_table(cursor)
    # main lookup
    check_prices_for_products(driver, conn, products)
    # close all connections
    tear_down(driver, conn)

# main lookup
def check_prices_for_products(driver, conn, products):
    for product in products:
        url = product.get("url")
        name = product.get("name")
        driver.get(url)
        price = get_element_by_xpath(driver, product.get("xpath"))
        if price:
            price = float(format_price(price.text))
            # add price to existing dict from json
            product["price"]=price
            if conn:
                database.insert_product(conn, product)
            else:
                # if no db connection
                print(product)
        else:
            print("Couldn't find price object for product: [{}{}]".format(name, url))

# surrounding in try catch when we need to call from multipel places
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

    driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
    return driver

def tear_down(driver, conn):
    print("Closing connection.")
    driver.quit()
    if conn: 
        conn.close()
    print("Connection closed.")

if __name__ == "__main__":
    main()