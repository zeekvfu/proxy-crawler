#!/usr/bin/python3
# coding: utf-8
# file_utility.py


import json
from collections import OrderedDict


# 按行读取文件，包括空行
def read_file_by_line(file_name, open_mode='r'):
    lines = []
    with open(file_name, encoding='utf-8', mode=open_mode) as f:
        while True:
            line = f.readline()
            if not line:
                break
            lines.append(line.rstrip('[\r\n]'))
    return lines


# 按行读取文件（行去重）
def read_unique_lines(file_name, open_mode='r'):
    unique_lines = []
    with open(file_name, encoding='utf-8', mode='r') as f:
        while True:
            line = f.readline()
            if not line:
                break
            line = line.rstrip('[\r\n]')
            if line in unique_lines:
                continue
            unique_lines.append(line)
    return unique_lines


# 读取配置文件
def read_config(file_name, open_mode='r'):
    with open(file_name, encoding='utf-8', mode=open_mode) as f:
        content = f.read()
        return eval(content)


# 读取 JSON 配置文件
def load_json_preserving_order(file_name, open_mode='r'):
    with open(file_name, encoding='utf-8', mode=open_mode) as f:
        content = f.read()
        # 保持 JSON 文件里 dict 原来的顺序
        return json.loads(content, object_pairs_hook=OrderedDict)


# 将字符串 s 写入文件
def write_to_file(file_name, s, open_mode='w'):
    with open(file_name, encoding='utf-8', mode=open_mode) as f:
        f.write(s)




