# Introduction
This service for collecting metrics from internal machine / exporter push to Pushgateway.
# Getting started

Some envionments need to config:
- SCRAP_INTERVAL: scrap time interval ,                                                 (default: 30s)
- PUSHGATEWAY_SERVER = pushgateway server url                                           (default: 'http://host.docker.internal:9091')
- EXPORTER_ENDPOINT: array exporter endpoint with format endpoint_url|job|instance      (default: 'http://host.docker.internal:9182/metrics|job1|instance1')
> For example EXPORTER_ENDPOINT=http://host.docker.internal:9182/metrics|window_exporter_job|my_computer,http://host.docker.internal:9090/metrics|prometheus_job|prometheus\
> Note that all label will overide the the label in pushgateway
## Run by docker
```
docker pull 2clicksolutions/pushservice:0.1
docker run -e pushservice.env 2clicksolutions/pushservice:0.1
```
## Run by docker-compose
```
docker pull 2clicksolutions/pushservice:0.1
docker-compose up -d

```
# Refer:
- https://github.com/prometheus/pushgateway
