#!/usr/bin/python3
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
        item['anonymity'] = ETL.normalize_anonymity(item['anonymity'])
        return item




