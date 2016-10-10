#!/usr/bin/env python3
# coding: utf-8
# pipelines.py


from scrapy.exceptions import DropItem


class ETL(object):

    @classmethod
    def normalize_anonymity(cls, _anonymity):
        anonymity = _anonymity.strip()
        if anonymity == "高匿名":
            anonymity = "highly anonymous"
        elif anonymity == "透明":
            anonymity = "transparent"
        return anonymity


    def process_item(self, item, spider):
        item['protocol'] = item['protocol'].strip()
        item['ip'] = item['ip'].strip()
        item['user_name'] = item['user_name'].strip()
        item['password'] = item['password'].strip()
        item['anonymity'] = ETL.normalize_anonymity(item['anonymity'])
        item['location'] = item['location'].strip()
        item['support_request_type'] = item['support_request_type'].strip()
        item['sp'] = item['sp'].strip()
        return item




