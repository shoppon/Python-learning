#! /usr/bin/python
import requests
from socket import gethostbyname
import logging
from logging import Formatter
from logging import StreamHandler
from logging.handlers import SysLogHandler

try:
    import syslog
except:
    syslog = None


def get_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    formatter = Formatter("%(asctime)s [%(module)s] %(message)s")

    stream_handler = StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    syslog_handler = SysLogHandler(
        address='/dev/log', facility=SysLogHandler.LOG_DAEMON)
    syslog_handler.setFormatter(formatter)
    logger.addHandler(syslog_handler)
    return logger


def get_current_dns():
    return gethostbyname('shoppon.site')


def get_current_ip():
    return requests.get('http://ip.cip.cc/').text.strip()


def config_dns(new_ip):
    resp = requests.put('https://api.godaddy.com/v1/domains/shoppon.site/records/A', json=[{
        'data': new_ip,
        'name': '@'
    }], headers={
        'accept': 'application/json',
        'X-Shopper-Id': '39039331',
        'Content-Type': 'application/json',
        'Authorization': 'sso-key 9Zw16udsgXS_7PpmdPmfM1UGATWUzV7zJC:Qg2Khs5jEMiRJAA627psJ7'
    })
    logger.info(f'Status: {resp.status_code}')


if __name__ == '__main__':
    logger = get_logger()
    my_ip = get_current_ip()
    dns_ip = get_current_dns()
    logger.info(f'My ip: {my_ip}, current dns: {dns_ip}')
    if my_ip != dns_ip:
        logger.info(f'Set dns ip: {my_ip}')
        config_dns(my_ip)
