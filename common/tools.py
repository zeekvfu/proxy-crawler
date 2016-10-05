#!/usr/bin/python3
# coding: utf-8
# tools.py


from bs4 import BeautifulSoup
from common.utility import random_elem, get_logger
from common.http_utility import get_homepage, user_agent_list, get_html_content


# 获取 IP 归属地（使用的是 ipip.net 的数据）
def ip_location_inquiry(logger, ip):
    if ip is None or len(ip) == 0:
        return

    url = "https://www.ipip.net/ip.html"
    post_data = {
            'ip': ip
            }
    referer = get_homepage(url)
    user_agent = random_elem(user_agent_list)

    result = get_html_content(logger, url, post_data, referer, user_agent)
    if result is None:
        return
    html_soup = BeautifulSoup(result[1], "html.parser")
    l = html_soup.select('tr > td[colspan="3"] > div > span[id="myself"]')
    if len(l) == 1:
        return l[0].string.strip()
    return


def generate_proxy_url(protocol, ip, port):
    _protocol = protocol.lower()
    return "%s://%s:%d" % (_protocol, ip, port)


def generate_proxy_tuple(protocol, ip, port):
    _protocol = protocol.lower()
    if _protocol != 'http' and _protocol != 'https':
        return
    return _protocol, generate_proxy_url(protocol, ip, port)


# 获取 proxy 的响应延迟（单位是 ms）
def get_response_delay(logger, url, protocol, ip, port):
    result = generate_proxy_tuple(protocol, ip, port)
    if result is None or len(result) != 2:
        return -1
    proxy_dict = {}
    proxy_dict[result[0]] = result[1]
    _user_agent = random_elem(user_agent_list)
    result = get_html_content(logger, url, user_agent=_user_agent, proxy=proxy_dict)
    if result is None:
        return
    return result[0]


if __name__ == '__main__':
    logger = get_logger('/tmp/tools.log')
    logger.info("****************************************************************************************************")
    logger.info("starting ...")

    ip = "205.252.220.20"
    result = ip_location_inquiry(logger, ip)
    logger.info("%s\t%s" % (ip, result))

    url = "https://www.baidu.com/"
    # url = "http://mindcache.io/"

    protocol = 'HTTP'
    ip = '45.32.36.87'
    port = 3128
    response_delay_in_ms = get_response_delay(logger, url, protocol, ip, port)
    logger.info("%s\t%f" % (generate_proxy_url(protocol, ip, port), response_delay_in_ms))

    protocol = 'HTTP'
    ip = '61.185.137.126'
    port = 3128
    response_delay_in_ms = get_response_delay(logger, url, protocol, ip, port)
    logger.info("%s\t%f" % (generate_proxy_url(protocol, ip, port), response_delay_in_ms))

    protocol = 'HTTP'
    ip = '221.229.204.231'
    port = 8080
    response_delay_in_ms = get_response_delay(logger, url, protocol, ip, port)
    logger.info("%s\t%f" % (generate_proxy_url(protocol, ip, port), response_delay_in_ms))

    protocol = 'HTTP'
    ip = '111.192.166.13'
    port = 9000
    response_delay_in_ms = get_response_delay(logger, url, protocol, ip, port)
    logger.info("%s\t%f" % (generate_proxy_url(protocol, ip, port), response_delay_in_ms))




