#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#  @namespace pymemcache-client

import os
import sys
from pprintpp import pprint

from pymemcache_client import (
    PymemcacheClient
)

def main():
    config = {
        "host": os.environ.get(f"PYMEMCACHE_HOST"),
        "port": os.environ.get(f"PYMEMCACHE_PORT"),
        "elastic_cache": os.environ.get(f"PYMEMCACHE_ELASTIC_CACHE"),
    }

    pymemcache_client = PymemcacheClient(config=config, product="example")
    pprint("Pymemcache Client: {0}".format(pymemcache_client.host))
    pprint("Cache Client: {0}".format(vars(pymemcache_client.cache_client)))

    for key in pymemcache_client.cache_client.clients:
        pprint(vars(pymemcache_client.cache_client.clients[key]))

if __name__ == '__main__':
    sys.exit(main())
