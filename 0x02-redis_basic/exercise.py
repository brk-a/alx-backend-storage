#!/usr/bin/env python3

'''
A class that stores an instance of redis client
as a private variable and stores data in redis.
'''

import redis
from uuid import uuid4
from typing import Union, Callable


class Cache:
    """defines methods that perform few common redis-py operations
       on redis
    """
    def __init__(self):
        """Instantiates a redis client"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Stores the data in redis"""
        r_key = str(uuid4())
        self._redis.set(r_key, data)
        return r_key

    def get(self, key: str, fn: Callable = None):
        """Calls a method that Converts redis data back to desired format"""
        data = self._redis.get(key)
        if fn is not None:
            return fn(data)
        return data
