import requests
import time
import os
import logging
import validators
import sys
from requests.auth import HTTPBasicAuth

SCRAP_INTERVAL = os.getenv('SCRAP_INTERVAL', 30)
EXPORTER_ENDPOINT = os.getenv('EXPORTER_ENDPOINT', 'http://host.docker.internal:9182/metrics|job1|instance1')
PUSHGATEWAY_SERVER = os.getenv('PUSHGATEWAY_SERVER', 'http://host.docker.internal:9091')
BASIC_AUTH_USERNAME = os.getenv('BASIC_AUTH_USERNAME', '')
BASIC_AUTH_PASSWD = os.getenv('BASIC_AUTH_PASSWD', '')

logging.basicConfig(level=logging.INFO,format="%(asctime)s - %(levelname)s - %(message)s")
def main():
    while True:
        if requests.get(PUSHGATEWAY_SERVER + '/-/ready',auth=HTTPBasicAuth(BASIC_AUTH_USERNAME, BASIC_AUTH_PASSWD)).status_code == 200:
            logging.info("Pushgateway is ready to serve traffic")
        elif requests.get(PUSHGATEWAY_SERVER + '/-/ready',auth=HTTPBasicAuth(BASIC_AUTH_USERNAME, BASIC_AUTH_PASSWD)).status_code == 401:
            logging.error("Unauthorization")
            exit(0)
        else:
            logging.error("Can't connect to Pushgateway.")
            exit(0)
        for e in EXPORTER_ENDPOINT.split(','):
            endpoint, job_name, instance_name = e.split('|')
            if ((validators.url(endpoint)) == True):
                try:
                    requests.get(endpoint).status_code == 200
                except:
                    logging.error("Can't get metric from {e}.".format(e=endpoint))
                    continue
                resp = requests.get(endpoint)
                response = requests.post('{p}/metrics/job/{j}/instance/{i}'.format(p=PUSHGATEWAY_SERVER, j=job_name, i=instance_name), data=resp.text)
                logging.info("Get metrics from {e} and push to Pushgateway.".format(e=endpoint))
            else:
                logging.error("Invalid exporter endpoint url {e}.".format(e=EXPORTER_ENDPOINT))
        time.sleep(int(SCRAP_INTERVAL))
if __name__ == '__main__':
    main()

