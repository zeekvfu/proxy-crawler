#!/usr/bin/env python3
# coding: utf-8
# ip_utility.py


import re
import ipaddress


class IP_Utility():

    # 0.0.0.0
    ip_int_min = int(ipaddress.IPv4Address('0.0.0.0'))
    # 255.255.255.255
    ip_int_max = int(ipaddress.IPv4Address('255.255.255.255'))


    ipv4_pattern = '\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
    # 127.0.0.1
    ipv4_single_regex = re.compile("^%s$" % (ipv4_pattern))
    # 192.0.2.0/29
    ipv4_subnet_regex = re.compile(r"^%s/\d{1,2}$" % (ipv4_pattern))
    # 192.168.0.1-192.168.0.2
    ipv4_range_regex = re.compile(r"^%s-%s$" % (ipv4_pattern, ipv4_pattern))

    ipv6_pattern = '\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'


    @staticmethod
    def get_ip_version(ip_segment):
        ip_version = None
        if re.match(IP_Utility.ipv4_single_regex, ip_segment) is not None or re.match(IP_Utility.ipv4_subnet_regex, ip_segment) is not None or re.match(IP_Utility.ipv4_range_regex, ip_segment) is not None:
            ip_version = 4
        return ip_version


    @staticmethod
    def gen_ipv4_range(ip_segment):
        if re.match(IP_Utility.ipv4_single_regex, ip_segment) is not None:
            return [ int(ipaddress.IPv4Address(ip_segment)) ]
        elif re.match(IP_Utility.ipv4_subnet_regex, ip_segment) is not None:
            return [ int(x) for x in ipaddress.ip_network(ip_segment).hosts() ]
        elif re.match(IP_Utility.ipv4_range_regex, ip_segment) is not None:
            start, end = ip_segment.split('-')
            start = int(ipaddress.IPv4Address(start))
            end = int(ipaddress.IPv4Address(end))
            if start <= end:
                return list(range(start, end+1))


    @staticmethod
    def get_ip_neighbors(ip, context=3):
        ip_int = None
        if isinstance(ip, int):
            ip_int = ip
        elif isinstance(ip, str):
            ip_int = int(ipaddress.IPv4Address(ip))
        start = max(IP_Utility.ip_int_min, ip_int - context)
        end = min(IP_Utility.ip_int_max, ip_int + context)
        return list(range(start, end+1))
        # return list(map(lambda x: ipaddress.IPv4Address(x), range(start, end+1)))


if __name__ == '__main__':
    print(IP_Utility.get_ip_neighbors('192.0.2.0'))

    print(IP_Utility.gen_ipv4_range('127.0.0.1'))
    print(IP_Utility.gen_ipv4_range('192.0.2.0/29'))
    print(IP_Utility.gen_ipv4_range('192.168.0.1-192.168.0.3'))




