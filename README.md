# Python Price Watcher

A python script to scrape prices for set of products and optionally store these in a local databse using selenium.

-   TODO: set up MySql instance
    -   Categorise into categories?
-   Once working set up cron job to run on schedule
-   Add some frontend or expose in startpage once made.

### Setup:

-   Install pip packages
-   Database instance (optional)
-   **config/config.json**: main config i.e. database sources and auth
-   **config/watchers.json**: actual products with links, names, and XPATH to watch.

### Notes

Selenium used instead of BeautifulSoup so we can change variants when URL path/params don't link to a specific size.
