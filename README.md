# Webcrawler storing online shop product prices

Project goal: track prices of products in online shops.

Online shops crawled:
- [Billa](shop.billa.at)

## Crawler

Everything in [./crawl-infra/](./crawl-infra/).

A webrawler that periodically download the data of online shop products, while hiding it's IP behind a VPN.

### Sesitive data

- [OpenVPN passfile](./crawl-infra/vpn/passfile) (not included in this repository)
- [OpenVPN configuration](./crawl-infra/vpn/config.ovpn) (not included in this repository)

### Deployment

Via docker, see [./crawl-infra/docker-compose.yaml](./crawl-infra/docker-compose.yaml)

## Online shop API exploration

Everything in [./api-exploration](./api-exploration/).

A collection of jupyter notebooks, scrips and data samples to explore the APIs of online shops.
