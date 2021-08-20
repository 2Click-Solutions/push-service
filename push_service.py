import requests
import time
import os
import logging
import validators
import sys

SCRAP_INTERVAL = os.getenv('SCRAP_INTERVAL', 30)
EXPORTER_ENDPOINT = os.getenv('EXPORTER_ENDPOINT', 'http://host.docker.internal:9182/metrics|job1|instance1')
PUSHGATEWAY_SERVER = os.getenv('PUSHGATEWAY_SERVER', 'http://host.docker.internal:9091')

logging.basicConfig(level=logging.INFO,format="%(asctime)s - %(levelname)s - %(message)s")
def main():
    try:
        requests.get(PUSHGATEWAY_SERVER + '/-/healthy').status_code == 200
    except:
        logging.error("Can't connect to Pushgateway {e}".format(e=PUSHGATEWAY_SERVER))
        exit(0)
    logging.info("Connected to Pushgateway")
    while True:
        for e in EXPORTER_ENDPOINT.split(','):
            endpoint, job_name, instance_name = e.split('|')
            if ((validators.url(endpoint)) == True):
                try:
                    requests.get(endpoint).status_code == 200
                except:
                    logging.error("Can't get metric from {e}".format(e=endpoint))
                    continue
                resp = requests.get(endpoint)
                response = requests.post('{p}/metrics/job/{j}/instance/{i}'.format(p=PUSHGATEWAY_SERVER, j=job_name, i=instance_name), data=resp.text)
                logging.info("Get metrics from {e} and push to {p}".format(e=endpoint,p=PUSHGATEWAY_SERVER))
            else:
                logging.error("Invalid exporter endpoint url {e}".format(e=EXPORTER_ENDPOINT))
        time.sleep(int(SCRAP_INTERVAL))
if __name__ == '__main__':
    main()

