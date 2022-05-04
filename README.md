# Product crawler

## Run the crawler (currently only billa)

```
$ pwd
/home/vbauer/Mega/Projects/BillaProducts
$ docker-compose -f docker-compose.yml up --build
...
```

## Watch progress

```
$ sudo ls /var/lib/docker/volumes/billaproducts_products/_data/billa/
20220504_121504_products.jl
```

Find latest file.

```
$ sudo wc -l /var/lib/docker/volumes/billaproducts_products/_data/billa/20220504_121504_products.jl
Every 1,0s: sudo wc -l /var/lib/docker/volumes/billaproducts_products/_data/billa/20220504_121504_products.jl

2102 /var/lib/docker/volumes/billaproducts_products/_data/billa/20220504_121504_products.jl
```
