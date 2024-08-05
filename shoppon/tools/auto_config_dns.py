#! /usr/bin/python
from logging import Formatter
from logging import StreamHandler
from socket import gethostbyname
import logging
import requests


def get_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    formatter = Formatter("%(asctime)s [%(module)s] %(message)s")

    stream_handler = StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger


def get_current_dns():
    return gethostbyname('shoppon.world')


def get_current_ip():
    return requests.get('http://jsonip.com').json().get('ip')


def config_dns(new_ip):
    resp = requests.put('https://api.name.com/v4/domains/shoppon.world/records/245149684', json={
        "host": "",
        "type": "A",
        "answer": new_ip,
        "ttl": 300
    }, headers={
        'accept': 'application/json',
        'Content-Type': 'application/json',
    }, auth=("shoppon", "{api token}"))
    logger.info(f'Status: {resp.status_code}')
    logger.info(f'Body: {resp.content}')


if __name__ == '__main__':
    logger = get_logger()
    my_ip = get_current_ip()
    dns_ip = get_current_dns()
    logger.info(f'My ip: {my_ip}, current dns: {dns_ip}')
    if my_ip != dns_ip:
        logger.info(f'Set dns ip: {my_ip}')
        config_dns(my_ip)
