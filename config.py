# -*- coding: utf-8 -*-
"""
调取配置文件和屏幕分辨率的代码
"""
import os
import sys
import json
import re


def open_brain_config():
    """
    调用配置文件
    """
    config_file = "brain.json"
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            print("Load config file from {}".format(config_file))
            return json.load(f)
    else:
        with open('config.json') as f:
            print("Load default config")
            return json.load(f)
