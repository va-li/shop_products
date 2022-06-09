# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import json
from scrapy.exceptions import DropItem

import sqlite3
import os
import time

class DuplicateProductDropPipeline:
    """
    Drops all products that have already been updated.
    """
    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        product = item
        product_id: str = product['articleId']
        
        if product_id in self.ids_seen:
            raise DropItem(f'Duplicate product found: "{product_id}"')
        else:
            self.ids_seen.add(product_id)
            return product

class StoreBillaProductPriceSqlite(object):
    """
    Takes the product and stuffs it into an sqlite database
    """
    def open_spider(self, spider):
        
        db_path         = os.getenv('PRODUCTS_BILLA_DB', '/home/vbauer/Mega/Projects/shop_products/crawl-infra/crawler/products/dev-data/products_billa.sqlite3')
        db_mode         = 'rw'
        db_uri          = f'file:{db_path}?mode={db_mode}'
        
        spider.logger.info(f'Using database URI {db_uri}')
        
        self.connection = sqlite3.connect(db_uri, uri=True)
        
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
        
        product_id: str = product['articleId']
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
            
            if product['_is_new']:
                values = [
                    product_id,
                    product['name'],
                    product['description'],
                    product['brand'],
                    product['category'],
                    product['product_group_id'],
                    product['grammage'],
                    product['vatCode'],
                    product['rank'],
                    json.dumps(product['attributes']),
                    json.dumps(product['eanCodes'])
                ]
                
                self.connection.execute(''' INSERT INTO products
                    (id, name, description, brand, category, product_group_id, grammage, vatCode, rank, attributes, eanCodes)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''',
                    values)
                
                spider.logger.debug(f'New product stored: "{product_id}"')
            
            self.connection.execute('''INSERT INTO prices
                (prod_id, timestamp, price_normal, price_sale)
                VALUES (?, ?, ?, ?)
                ''',
                [ product_id, unix_time_now, price_normal, price_sale ])

        spider.logger.debug(f'Product price stored for "{product_id}"')
        return product
