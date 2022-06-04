from typing import List
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
        
        # get all product ids stored in the database
        connection  = sqlite3.connect(db_uri, uri=True)
        rows = connection.execute('SELECT id FROM products').fetchall()
        self.existing_product_ids = [ r[0] for r in rows ]
        connection.close()
        
        # get all product groups
        with open('./resources/smallest_product_groups.json', 'r') as file:
            product_groups: List[str] = json.load(file)
        
        # request all product groups
        for g_id in product_groups:
            yield scrapy.Request(
                url=f'https://shop.billa.at/api/search/full?category={g_id}',
                callback=self.parse_category_search_result,
                meta={ 'product_group_id': g_id, 'page': 1 })
    
    def parse_category_search_result(self, response):
        product_group_id = response.meta['product_group_id']
        page = response.meta['page']
        
        json_response = json.loads(response.text)
            
        if not json_response['pagingInfo']['isLastPage']:
            next_page = page + 1
            yield scrapy.Request(
                    url=f'https://shop.billa.at/api/search/full?category={product_group_id}&page={next_page}',
                    callback=self.parse_category_search_result,
                    meta={ 'product_group_id': product_group_id, 'page': next_page })
        
        for obj in json_response['tiles']:
            try:
                if obj['type'] != 'product':
                    continue
                
                product = obj['data']
                product_id = product['articleId']
                
                if product_id in self.existing_product_ids:
                    # mark product as not new, so only the price will be updated
                    product['_is_new'] = False
                    yield product
                else:
                    # when a new product is found, request the details
                    yield scrapy.Request(
                        url=f'https://shop.billa.at/api/articles/{product_id}',
                        callback=self.parse_product_details,
                        meta={ 'product_group_id': product_group_id })
                
            except KeyError as e:
                self.logger.info(f'While searching articles in product group "{response.meta["product_group_id"]}", failed to parse article ids: KeyError {e}')
                continue
            
    def parse_product_details(self, response):
        # mark product as new, because we requested the details of this particular product
        product = json.loads(response.text)
        product['_is_new'] = True
        product['product_group_id'] = response.meta['product_group_id']
        yield product
