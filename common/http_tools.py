#!/usr/bin/python3
# coding: utf-8
# http_tools.py


import random
import json
import http.client
import urllib.error
from bs4 import BeautifulSoup

from common.utility import get_logger
from common.http_utility import get_homepage, user_agent_list, get_html_content


# 获取 IP 归属地（使用的是 ipip.net 的数据）
def ip_location_inquiry(logger, ip):
    logger.debug("ip_location_inquiry(): start ...")
    if ip is None or len(ip) == 0:
        return

    url = "https://www.ipip.net/ip.html"
    post_data = {
            'ip': ip
            }
    referer = get_homepage(url)
    user_agent = random.choice(user_agent_list)

    result = get_html_content(logger, url, post_data, referer, user_agent)
    if result[0] == -1:
        return
    html_soup = BeautifulSoup(result[1], "html.parser")
    l = html_soup.select('tr > td[colspan="3"] > div > span[id="myself"]')
    if len(l) == 1:
        return l[0].string.strip()
    return


def generate_proxy_url(protocol, ip, port):
    _protocol = protocol.lower()
    return "%s://%s:%d" % (_protocol, ip, port)


def generate_proxy_pair(protocol, ip, port):
    _protocol = protocol.lower()
    if _protocol != 'http' and _protocol != 'https':
        return
    return _protocol, generate_proxy_url(protocol, ip, port)


# 获取 proxy 的响应延迟（单位是 ms）
def get_response_delay(logger, url, protocol, ip, port, retry=4):
    logger.debug("get_response_delay(): start ...")
    proxy = generate_proxy_pair(protocol, ip, port)
    if proxy is None or len(proxy) != 2:
        return
    logger.debug("get_response_delay(): proxy URL\t%s" % proxy[1])
    _user_agent = random.choice(user_agent_list)
    l = []
    for index in range(retry, 0, -1):
        logger.debug("get_response_delay(): index\t%d" % index)
        result = get_html_content(logger, url, user_agent=_user_agent, proxy_pair=proxy)
        if result[0] == -1:
            logger.debug("get_response_delay(): exception type\t%s" % type(result[1]))
            if isinstance(result[1], (urllib.error.HTTPError, urllib.error.URLError, http.client.InvalidURL, TypeError)):
                break
            else:
                continue
        l.append(result[0])
        logger.debug("get_response_delay(): index: %d\tresponse delay: %f" % (index, result[0]))
    logger.debug("get_response_delay(): response delay records\t%s" % json.dumps(l, ensure_ascii=False))
    if len(l) > 0:
        return sum(l)/len(l)


if __name__ == '__main__':
    logger = get_logger('/tmp/http_tools.log')
    logger.info("****************************************************************************************************")
    logger.info("start ...")

    ip = "205.252.220.20"
    result = ip_location_inquiry(logger, ip)
    logger.info("%s\t%s" % (ip, result))

    # url = "https://www.baidu.com/"
    url = "http://mindcache.io/"
    # url = "https://twitter.com/"

    protocol = 'HTTP'
    ip = '45.32.36.87'
    port = 31288
    response_delay_in_ms = get_response_delay(logger, url, protocol, ip, port)
    if response_delay_in_ms is not None:
        logger.info("%s\t%f" % (generate_proxy_url(protocol, ip, port), response_delay_in_ms))

    protocol = 'HTTPS'
    ip = '45.32.36.87'
    port = 31299
    response_delay_in_ms = get_response_delay(logger, url, protocol, ip, port)
    if response_delay_in_ms is not None:
        logger.info("%s\t%f" % (generate_proxy_url(protocol, ip, port), response_delay_in_ms))




