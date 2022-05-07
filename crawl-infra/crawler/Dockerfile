FROM python:3-slim

WORKDIR /crawler

# apt can't find packages if we don't update the sources first
RUN apt-get update -y
# scrapy needs tkinter
RUN apt-get install -y python3-tk

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD sleep $SCRAPY_DELAY && scrapy crawl billa_product_prices
