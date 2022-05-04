# Product crawler

## Run the crawler (currently only billa)

```
$ pwd
/home/vbauer/Mega/Projects/shop_products
$ docker-compose up --build
...
```

## Watch progress

```
$ sudo ls /var/lib/docker/volumes/crawl-infra_crawler_downloads/_data/billa
20220504_152756_products.jl
```

Find latest file.

```
$ watch -n 1 "sudo wc -l  /var/lib/docker/volumes/crawl-infra_crawler_downloads/_data/billa/20220504_152756_products.jl"
Every 1,0s: sudo wc -l  /var/lib/docker/volumes/crawl-infra_crawler_downloads/_data/billa/20220504_152756_products.jl

132 /var/lib/docker/volumes/crawl-infra_crawler_downloads/_data/billa/20220504_152756_products.jl
```
