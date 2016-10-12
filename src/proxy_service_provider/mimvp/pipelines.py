#!/usr/bin/env python3
# coding: utf-8
# pipelines.py


from scrapy.exceptions import DropItem


class ETL(object):

    def process_item(self, item, spider):
        item['protocol'] = item['protocol'].strip()
        item['ip'] = item['ip'].strip()
        item['user_name'] = item['user_name'].strip()
        item['password'] = item['password'].strip()
        item['anonymity'] = item['anonymity']
        item['location'] = item['location'].strip()
        item['support_request_type'] = item['support_request_type'].strip()
        item['sp'] = item['sp'].strip()
        return item




