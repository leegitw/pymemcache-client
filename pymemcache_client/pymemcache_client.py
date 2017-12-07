#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#  @copyright 2017 TUNE, Inc. (http://www.tune.com)
#  @namespace pymemcache-client

import os
import ujson as json
import telnetlib
import re
from pymemcache.client.hash import HashClient
# from pprintpp import pprint

class PymemcacheClient(object):
    def __init__(self, config=None, product=None, required_fields=None, config_file=None, **kwargs):
        """Prepare a Pymemcache Client using available configuration for host, port, and if available
        elastic_cache.

        Keyword arguments:
        config
        product
        required_fields
        config_file
        """

        if config is None:
            config = {
                "host": None,
                "port": None,
                "elastic_cache": None,
            }

        try:
            config = configFromFile(config, os.path.expanduser("~/.pymemcache.json"))
        except:
            pass

        config = configFromEnv(config)
        config = configFromEnv(config, product)
        config = configFromFile(config, "pymemcache.json", product)
        config = configFromFile(config, config_file, product)
        config = configFromArgs(config, **kwargs)

        if required_fields is None:
            required_fields = ["host", "port"]

        for field in required_fields:
            if config[field] is None:
                raise ValueError("No %s set. %s is a required field." % (field, field))

        for k, v in config.items():
            setattr(self, k, v)

        if "elastic_cache" in config and config["elastic_cache"]:
            self.cache_servers = self.aws_elasticache_endpoints(config["host"], config["port"])
        else:
            self.cache_servers = [(config["host"], config["port"])]

        self.cache_error = None
        self.cache_client = HashClient(servers=self.cache_servers)

    def aws_elasticache_endpoints(self, host, port):
        # We're using elasticache cache engine >= 1.4.14 "config get" must be used
        # http://docs.aws.amazon.com/AmazonElastiCache/latest/UserGuide/AutoDiscovery.AddingToYourClientLibrary.html

        command = "config get cluster\n".encode('ascii')
        tn = telnetlib.Telnet(host, port)
        tn.write(command)
        ret = tn.read_until(b"END").decode("utf-8")
        tn.close()

        p = re.compile(r'\r?\n')
        conf = p.split(ret)

        servers = []

        if len(conf) != 5 or conf[4] != 'END':
            raise ValueError("Invalid discovery response")

        nodes_str = conf[2].split(' ')
        for node_str in nodes_str:
            node_list = node_str.split('|')  # host|ip|port
            if len(node_list) != 3:
                raise ValueError("Invalid cluster configuration")
            servers.append((node_list[1], int(node_list[2])))

        return servers


def configFromFile(config, path, product=None):
    if path is None:
        return config
    if not os.path.exists(path):
        return config
    try:
        file = open(path, "r")
    except IOError:
        return config

    raw = json.loads(file.read())
    file.close()

    for k in raw.keys():
        if k in config:
            config[k] = raw[k]
    if product is not None:
        if product in raw:
            for k in raw[product].keys():
                config[k] = raw[product][k]
    return config


def configFromEnv(config, product=None):
    if product is None:
        product = "pymemcache"
    for k in config.keys():
        key = "%s_%s" % (product, k)
        if key.upper() in os.environ:
            config[k] = os.environ[key.upper()]
    return config


def configFromArgs(config, **kwargs):
    for k in kwargs:
        if kwargs[k] is not None:
            config[k] = kwargs[k]
    return config


def intersect(a, b):
    return list(set(a) & set(b))
