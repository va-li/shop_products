FROM python:3-slim

WORKDIR /usr/src/app

# apt can't find packages if we don't update the sources first
RUN apt-get update -y
# scrapy needs tkinter
RUN apt-get install -y python3-tk

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD scrapy crawl billa_products -O ./shop_products/data/billa/$(date +"%Y%m%d_%H%M%S")_products.jl
