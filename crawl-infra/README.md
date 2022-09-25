# Shop product webcrawler components

## Crawler

Everything in [./crawler/](./crawler/).

A docker image using python [Scrapy](https://scrapy.org/) to crawl online shop websites. The crawler is periodically executed by leveraging cron inside the docker container.

## VPN

Everything in [./vpn/](./vpn/).

A docker image connecting to an OpenVPN server to hide the IP of the server running the crawler program, so my server does not get blocked by any online shop websites. Leverages the pre-made docker image [ghcr.io/wfg/openvpn-client](ghcr.io/wfg/openvpn-client) to tunnel all network traffic through OpenVPN.

## Tying VPN and Crawler together

Happens in the [./docker-compose.yaml](./docker-compose.yaml) by putting the crawler docker container and the vpn docker container on the same virtual network.

```yaml
services:
  openvpn-client:
    ...
  crawler:
    network_mode: service:openvpn-client
    ...
```
