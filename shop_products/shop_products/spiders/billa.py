from itertools import product
from turtle import down
import scrapy
import json


class BillaProductsSpider(scrapy.Spider):
    name = 'billa_products'

    def start_requests(self):
        yield scrapy.Request('http://checkip.dyndns.org/', callback=self.log_ip)
        
        product_groups = None
        with open('./billa_product_groups_flat.json', 'r') as file:
            product_groups = json.load(file)
        
        for g_name, g in product_groups.items():
            if g['is_leaf']:
                yield scrapy.Request(
                    url=f'https://shop.billa.at/api/search/full?category={g["id"]}',
                    callback=self.parse_search_result,
                    meta={ 'product_group': g, 'page': 1 })
        
        ''' small set of prods for testing
        yield scrapy.Request(
                    url=f'https://shop.billa.at/api/search/full?category=B2-E2',
                    callback=self.parse_search_result,
                    meta={ 'product_group': {'id': 'B2-E2'}, 'page': 1 })
        '''

    def log_ip(self, response):
        pub_ip = response.xpath('//body/text()').re('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')[0]
        self.logger.info(f'Crawler\'s public IP is: {pub_ip}')
        
    
    def parse_search_result(self, response):
        product_group = response.meta['product_group']
        page = response.meta['page']
        
        json_response = json.loads(response.text)
            
        if not json_response['pagingInfo']['isLastPage']:
            next_page = page + 1
            yield scrapy.Request(
                    url=f'https://shop.billa.at/api/search/full?category={product_group["id"]}?page={next_page}',
                    callback=self.parse_search_result,
                    meta={ 'product_group': product_group, 'page': next_page })
        
        for obj in json_response['tiles']: 
            try:
                articleId = obj['data']['articleId']
                yield scrapy.Request(
                    url=f'https://shop.billa.at/api/articles/{articleId}',
                    callback=self.parse_product,
                    meta={ 'product_group': product_group })
            except KeyError as e:
                self.logger.info(f'While searching articles in product group "{response.meta["product_group"]["id"]}", failed to parse article ids: {e}')
                continue
    
    def parse_product(self, response):
        json_response = json.loads(response.text)
        json_response['productGroup'] = response.meta['product_group']
        yield json_response
