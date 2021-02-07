# Database setup and queries if applicable
import os
import mysql.connector
from mysql.connector import errorcode
from datetime import date, datetime

env = os.environ

def connect():
    # Database config stored as environment variables
    conn = mysql.connector.connect(user=env.get('PRICEWATCH_MYSQL_USER'), 
                              password=env.get('PRICEWATCH_MYSQL_PASS'),
                              host=env.get('PRICEWATCH_MYSQL_HOST'),
                              database=env.get('PRICEWATCH_MYSQL_DATABASE'))
    return conn

def create_table(cursor):
    create_table_query = (
        "CREATE TABLE `prices` ("
        "`id` int(11) NOT NULL AUTO_INCREMENT,"
        "`name` VARCHAR(100) NOT NULL,"
        "`date` DATETIME NOT NULL,"
        "`url` VARCHAR(300) NOT NULL,"
        "`price` FLOAT NOT NULL,"
        "`category` VARCHAR(50),"
        "PRIMARY KEY(id)"
        ") ENGINE=InnoDB"
    )
    try:
        cursor.execute(create_table_query)
        print("Created prices table.")
    except mysql.connector.Error as err:
        # If already setup we'll just connect to existing table
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("Using existing prices table.")
        else:
            print(err.msg)
    else:
        print("price table created")

def insert_product(conn, product):
    product["lookup_date"] = datetime.now()
    insert_query = (
        "INSERT INTO prices (name, date, url, price, category)"
        "VALUES ('{}','{}','{}',{},'{}')"
            .format(product.get("name"), product.get("lookup_date"),
                product.get("url"), product.get("price"), product.get("category")
            )
    )
    try:
        cursor = conn.cursor()
        cursor.execute(insert_query)
        # on successfull execution, commit the transaction
        conn.commit()
        print("Added price entry: {}".format(product))
    except mysql.connector.Error as err:
        print(err.msg)
        conn.rollback()

def quit(conn):
    conn.close()