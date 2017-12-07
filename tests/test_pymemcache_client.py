#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#  @copyright 2017 TUNE, Inc. (http://www.tune.com)
#  @namespace pymemcache-client

import os
from pymemcache.client.hash import HashClient

from pymemcache_client import (
    PymemcacheClient
)

class TestPymemcacheClient():
    def test_pymemcache_client(self):
        config = {
            "host": os.environ.get(f"PYMEMCACHE_HOST"),
            "port": os.environ.get(f"PYMEMCACHE_PORT"),
            "elastic_cache": os.environ.get(f"PYMEMCACHE_ELASTIC_CACHE"),
        }

        pymemcache_client = PymemcacheClient(config=config, product="example")
        assert(pymemcache_client)

        assert(pymemcache_client.host == config['host'])
        assert(pymemcache_client.port == config['port'])
        assert(pymemcache_client.elastic_cache == config['elastic_cache'])

        assert(pymemcache_client.cache_error is None)
        assert(len(pymemcache_client.cache_servers) == 1)

        assert(pymemcache_client.cache_client)
        assert(type(pymemcache_client.cache_client) == HashClient)
