#!/usr/bin/env python3
# coding: utf-8
# items.py


from scrapy.item import Item, Field


class ProxyItem(Item):
    protocol = Field(default="", type="str")
    ip = Field(default="", type="str")
    port = Field(default=None, type="int")
    user_name = Field(default="", type="str")
    password = Field(default="", type="str")
    anonymity = Field(default="", type="str")
    support_request_type = Field(default="", type="str")
    location = Field(default="", type="str")
    sp = Field(default="", type="str")
    validation_time = Field(default="", type="str")
    source_site = Field(default="", type="str")
    source_url = Field(default="", type="str")




