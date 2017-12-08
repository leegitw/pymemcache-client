#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#  @copyright 2017 TUNE, Inc. (http://www.tune.com)
#  @namespace pymemcache-client

import os
from pymemcache.client.base import Client
from pymemcache.client.hash import HashClient
from pymemcache_client import PymemcacheClient

class TestPymemcacheClient():
    def test_pymemcache_client_none(self):
        pymemcache_client = PymemcacheClient(config=None)
        assert(pymemcache_client)

        assert(pymemcache_client.memcached_servers)
        assert(len(pymemcache_client.memcached_servers) == 1)
        assert(pymemcache_client.cache_error is None)

        assert(pymemcache_client.cache_client)
        assert(type(pymemcache_client.cache_client) is Client)

    def test_pymemcache_client_basic_default(self):
        config = {
            "servers": [{"host": "localhost", "port": 11211}]
        }

        pymemcache_client = PymemcacheClient(config=config)
        assert(pymemcache_client)

        assert(pymemcache_client.memcached_servers)
        assert(len(pymemcache_client.memcached_servers) == 1)
        assert(pymemcache_client.cache_error is None)

        assert(pymemcache_client.cache_client)
        assert(type(pymemcache_client.cache_client) is Client)

    def test_pymemcache_client_basic(self):
        config = {
            "servers": [{"host": "localhost", "port": 11211}], "client_type": "basic"
        }

        pymemcache_client = PymemcacheClient(config=config)
        assert(pymemcache_client)

        assert(pymemcache_client.memcached_servers)
        assert(len(pymemcache_client.memcached_servers) == 1)
        assert(pymemcache_client.cache_error is None)

        assert(pymemcache_client.cache_client)
        assert(type(pymemcache_client.cache_client) is Client)

    def test_pymemcache_client_hash(self):
        config = {
            "servers": [{"host": "localhost", "port": 11211}], "client_type": "hash"
        }

        pymemcache_client = PymemcacheClient(config=config)
        assert(pymemcache_client)

        assert(pymemcache_client.memcached_servers)
        assert(len(pymemcache_client.memcached_servers) == 1)
        assert(pymemcache_client.cache_error is None)

        assert(pymemcache_client.cache_client)
        assert(type(pymemcache_client.cache_client) is HashClient)


    def test_pymemcache_client_file(self):

        full_path = os.path.realpath(__file__)
        path = os.path.dirname(full_path)
        config_file = "{}/resources/test_pymemcache.json".format(path)

        pymemcache_client = PymemcacheClient(config_file=config_file)
        assert(pymemcache_client)

        assert(pymemcache_client.memcached_servers)
        assert(len(pymemcache_client.memcached_servers) == 1)
        assert(pymemcache_client.cache_error is None)

        assert(pymemcache_client.cache_client)
        assert(type(pymemcache_client.cache_client) is HashClient)