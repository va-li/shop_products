# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


from scrapy.exceptions import DropItem

import sqlite3
import os
import time

# This pipeline takes the Item and stuffs it into scrapedata.db
class StoreBillaProductPriceSqlite(object):
    def open_spider(self, spider):
        
        db_path         = os.getenv('PRODUCTS_BILLA_DB', '/home/vbauer/Mega/Projects/shop_products/crawl-infra/crawler/products/dev-data/products_billa.sqlite3')
        db_mode         = 'rw'
        db_uri          = f'file:{db_path}?mode={db_mode}'
        
        spider.logger.info(f'Using database URI {db_uri}')
        
        self.connection = sqlite3.connect(db_uri, uri=True)
        #self.cursor = self.connection.cursor()
        
        self.connection.execute('''
            CREATE TABLE IF NOT EXISTS prices (
                prod_id TEXT NOT NULL,
                timestamp INTEGER NOT NULL,
                price_normal REAL NOT NULL,
                price_sale REAL,
                PRIMARY KEY (prod_id, timestamp),
                FOREIGN KEY (prod_id) REFERENCES products(id))
            ''')

    def process_item(self, item, spider):
        product         = item
        unix_time_now   = int(time.time())
        
        if ('articleId' not in product or len(product['articleId']) == 0):
            raise DropItem('Missing articleId')
        
        articleId: str = product['articleId']
        
        try:
            price_normal = float(product['price']['normal'])
        except ValueError:
            raise DropItem('Malformed value for normal price')
        except KeyError:
            raise DropItem('Missing normal price')
        
        try:
            price_sale = float(product['price']['sale'])
        except (ValueError, KeyError):
            price_sale = None
        
        with self.connection:
            self.connection.execute('''
                INSERT INTO prices (prod_id, timestamp, price_normal, price_sale)
                VALUES (?, ?, ?, ?)
                ''',
                (articleId, unix_time_now, price_normal, price_sale))

        spider.logger.debug(f'Product price stored for "{articleId}"')
        return product
