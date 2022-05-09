#!/bin/bash

WEB_ENTRY_IP=$(wget -qO - ifconfig.me)
echo "Web entry point IP: $WEB_ENTRY_IP"

cd /crawler

/usr/local/bin/scrapy crawl billa_product_prices
