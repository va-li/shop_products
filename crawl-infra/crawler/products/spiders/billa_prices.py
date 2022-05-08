import scrapy
import json
import os
import sqlite3

class BillaProductsSpider(scrapy.Spider):
    name = 'billa_product_prices'
    download_timeout = 5
    
    def start_requests(self):
        
        db_path     = os.getenv('PRODUCTS_BILLA_DB', '/home/vbauer/Mega/Projects/shop_products/crawl-infra/crawler/products/dev-data/products_billa.sqlite3')
        db_mode     = 'ro'
        db_uri      = f'file:{db_path}?mode={db_mode}'
        
        self.logger.info(f'Using database URI {db_uri}')
        
        connection  = sqlite3.connect(db_uri, uri=True)
                
        product_ids = connection.execute('SELECT DISTINCT id FROM products').fetchall()
        
        connection.close()
        
        for product_id in product_ids:
            yield scrapy.Request(
                    url=f'https://shop.billa.at/api/articles/{product_id[0]}',
                    callback=self.parse_product)
    
    def parse_product(self, response):
        json_response = json.loads(response.text)
        yield json_response
