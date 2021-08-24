# Introduction
This service for collecting metrics from machine/exporter in internal network and pushing to Pushgateway.
# Getting started
## Overview:
![GitHub Logo](/push-service.png)

## Some envionments need to config:
| Enviroment variable | Description | Default value|
| ------ | ------ |-----|
|SCRAP_INTERVAL|scrap time interval|  30s |
|PUSHGATEWAY_SERVER|Pushgateway server url|http://host.docker.internal:9091|
|BASIC_AUTH_USERNAME|Pushgateway server basic authentication username|None|
|BASIC_AUTH_PASSWD|Pushgateway server basic authentication password|None|
|EXPORTER_ENDPOINT|array exporter endpoint with format ```endpoint_url|job|instance``` separate by comma ',' |http://host.docker.internal:9182/metrics|job1|instance1|

> For example:\
> EXPORTER_ENDPOINT=http://host.docker.internal:9182/metrics|window_exporter_job|my_computer,http://host.docker.internal:9090/metrics|prometheus_job|prometheus\
## Run by docker
```
docker pull 2clicksolutions/pushservice:0.2
docker run -e pushservice.env 2clicksolutions/pushservice:0.2
```
## Run by docker-compose
```
docker pull 2clicksolutions/pushservice:0.2
docker-compose up -d

```
# Refer:
- https://github.com/prometheus/pushgateway
