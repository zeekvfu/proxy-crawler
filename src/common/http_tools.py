#!/usr/bin/env python3
# coding: utf-8
# http_tools.py


import sys
import random
import http.client
import urllib.error
import IP
from bs4 import BeautifulSoup

from common.utility import get_logger
from common.http_utility import get_homepage_url, pc_browser_ua, test_port_open, get_html_content


# 查询 IP 归属地（使用的是 ipip.net 的数据）
def inquire_ip_location(logger, ip):
    this_func_name = sys._getframe().f_code.co_name
    logger.debug("%s(): start ..." % this_func_name)
    if ip is None or len(ip) == 0:
        return

    url = "https://www.ipip.net/ip.html"
    post_data = {
            'ip': ip
            }
    referer = get_homepage_url(url)
    user_agent = random.choice(pc_browser_ua)

    result = get_html_content(logger, url, post_data, referer, user_agent)
    if result[0] == -1 or result[1] is None:
        return
    html_soup = BeautifulSoup(result[1], "html.parser")
    l = html_soup.select('tr > td[colspan="3"] > div > span[id="myself"]')
    if len(l) == 1:
        return l[0].string.strip()
    logger.debug("%s(): end ..." % this_func_name)
    return


# 查询 IP 归属地。如果查不到该 IP 的话，则使用原来的归属地
def ipip_inquire_location(ip, old_location=None):
    new_location = IP.find(ip)
    if new_location is None:
        new_location = old_location
    return new_location


def generate_proxy_url(protocol, ip, port):
    protocol = protocol.lower()
    return "%s://%s:%d" % (protocol, ip, port)


def generate_proxy_pair(protocol, ip, port):
    protocol = protocol.lower()
    if protocol != 'http' and protocol != 'https':
        return
    return protocol, generate_proxy_url(protocol, ip, port)


# 获取 proxy 的响应延迟（单位是 ms）
def get_proxy_delay(logger, url, protocol, ip, port, retry=4):
    this_func_name = sys._getframe().f_code.co_name
    logger.debug("%s(): start ..." % this_func_name)
    proxy = generate_proxy_pair(protocol, ip, port)
    if proxy is None or len(proxy) != 2:
        return
    logger.debug("%s(): proxy URL\t%s" % (this_func_name, proxy[1]))
    _user_agent = random.choice(pc_browser_ua)
    l = []
    for index in range(retry, 0, -1):
        result = get_html_content(logger, url, user_agent=_user_agent, proxy_pair=proxy)
        if result[0] == -1:
            logger.debug("%s(): exception type\t%s" % (this_func_name, type(result[1])))
            if isinstance(result[1], (urllib.error.HTTPError, urllib.error.URLError, http.client.InvalidURL, TypeError)):
                break
            else:
                continue
        l.append(result[0])
        logger.debug("%s(): index: %d\tresponse delay: %f" % (this_func_name, index, result[0]))
    logger.debug("%s(): response delay records\t%s" % (this_func_name, str(l)))
    if len(l) > 0:
        average = round(sum(l)/len(l), 1)
        logger.debug("%s(): response delay average\t%f" % (this_func_name, average))
        return average
    return


if __name__ == '__main__':
    logger = get_logger('/tmp/http_tools.log')
    logger.info("****************************************************************************************************")
    logger.info("start ...")

    ip = "205.252.220.20"
    result = inquire_ip_location(logger, ip)
    logger.info("%s\t%s" % (ip, result))

    test_port_open(logger, '45.32.36.87', 312888)
    test_port_open(logger, '45.32.36.87', 8888)

    # url = "https://www.baidu.com/"
    url = "http://mindcache.io/"
    # url = "https://twitter.com/"

    protocol = 'HTTP'
    ip = '45.32.36.87'
    port = 31288
    response_delay_in_ms = get_proxy_delay(logger, url, protocol, ip, port)
    if response_delay_in_ms is not None:
        logger.info("%s\t%f" % (generate_proxy_url(protocol, ip, port), response_delay_in_ms))

    protocol = 'HTTPS'
    ip = '45.32.36.87'
    port = 31299
    response_delay_in_ms = get_proxy_delay(logger, url, protocol, ip, port)
    if response_delay_in_ms is not None:
        logger.info("%s\t%f" % (generate_proxy_url(protocol, ip, port), response_delay_in_ms))




