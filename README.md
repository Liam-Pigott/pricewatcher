# Python Price Watcher

A python script used to scrape prices for a set of products and optionally store these in a local database.

### Setup:

-   **Install pip packages** from **_requirements.txt_**

    > pip install -r requirements.txt

-   **config/config.json**: main config i.e. browser driver path and toggle to use a database instance.<br>

-   **config/products.json**: products to watch with links, names, and XPATH for prices.

-   **Database instance (optional)**
    -   Create or connect to an existing database and point the _database.py_ config to your instance. During setup the script will create a dedicated table for price watching.
    -   Out of the box the script uses environment variables for database auth. You can set environment variables according to the code below or change this setup by replacing the following in _database.py_:
    ```python
        conn = mysql.connector.connect(user=env.get('PRICEWATCH_MYSQL_USER'),
                              password=env.get('PRICEWATCH_MYSQL_PASS'),
                              host=env.get('PRICEWATCH_MYSQL_HOST'),
                              database=env.get('PRICEWATCH_MYSQL_DATABASE'))
    ```

### Notes

I've set this up as a cron job scheduled to run daily. If using the environment variable approach you'll need to make sure the task can access the appropraite environment variables. I used the following to set up a daily schedule to run at 9pm:

```bash
env | sudo tee /etc/environment
crontab -e
# Add the following to crontab
0 21 * * * /usr/bin/python <path_to_pricwatcher_project>/pricewatcher.py
```
