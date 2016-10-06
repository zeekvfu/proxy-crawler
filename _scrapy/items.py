#!/usr/bin/python3
# coding: utf-8
# items.py


from scrapy.item import Item, Field


class ProxyItem(Item):
    protocol = Field(default="", type="str")
    ip = Field(default="", type="str")
    port = Field(default=0, type="int")
    user_name = Field(default="", type="str")
    password = Field(default="", type="str")
    anonymity = Field(default="", type="str")
    support_request_type = Field(default="", type="str")
    location = Field(default="", type="str")
    sp = Field(default="", type="str")
    site_0_delay = Field(default=0, type="float")
    site_1_delay = Field(default=0, type="float")
    site_2_delay = Field(default=0, type="float")
    site_3_delay = Field(default=0, type="float")
    validation_time = Field(default="", type="str")
    source = Field(default="", type="str")




