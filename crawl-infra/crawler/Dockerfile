FROM python:3-slim

WORKDIR /usr/src/crawler

# apt can't find packages if we don't update the sources first
RUN apt-get update -y
# scrapy needs tkinter
RUN apt-get install -y python3-tk

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p ./downloads/billa

CMD scrapy crawl billa_product_details -O ./downloads/billa/products_metadata_$(date +"%Y%m%d_%H%M%S").jl
