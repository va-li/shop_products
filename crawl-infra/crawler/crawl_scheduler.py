import logging
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor
from scrapy.utils.project import get_project_settings
import requests
from os import getenv, system
from time import sleep
import schedule
from datetime import datetime

logger = logging.getLogger('crawl_scheduler')
logger.setLevel(logging.DEBUG)
sh = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s [%(name)s] %(levelname)s: %(message)s', '%Y-%m-%d %H:%M:%S')
sh.setFormatter(formatter)
logger.addHandler(sh)

INITIAL_SCHEDULE_DELAY = int(getenv('INITIAL_SCHEDULE_DELAY', 0))
CHECK_SCHEDULE_INTERVAL = int(getenv('CHECK_SCHEDULE_INTERVAL', 5))

logger.info(f'Waiting {INITIAL_SCHEDULE_DELAY} seconds (initial schedule delay)...')
sleep(INITIAL_SCHEDULE_DELAY)



def crawl():
    logger.info(f'Crawl started at {datetime.now()}')

    res = requests.get('https://api.ipify.org', timeout=10)

    if res.status_code != 200:
        logger.error(f'Failed to get IP address from https://api.ipify.org: {res.reason}')
        res.raise_for_status()

    ip_address = res.text
    logger.info(f'Web entry IP address: {ip_address}')

    # run crawl in subshell
    system('scrapy crawl billa_product_prices')



# Schedule crawl

schedule.every().day.at('06:00').do(crawl)

schedule.run_all()

while True:
    schedule.run_pending()
    sleep(CHECK_SCHEDULE_INTERVAL)
