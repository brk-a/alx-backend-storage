#!/usr/bin/env python3

'''
A class that stores an instance of redis client
as a private variable and stores data in redis.
'''

import redis
from uuid import uuid4
from typing import Union, Callable
from functools import wraps


def replay(method: Callable) -> None:
    """displays the history of calls of a particular function."""
    redis = method.__self__._redis
    qualified_name = method.__qualname__
    num_of_calls = redis.get(qualified_name).decode("utf-8")
    print("{} was called {} times:".format(qualified_name, num_of_calls))
    input_key = qualified_name + ":inputs"
    output_key = qualified_name + ":outputs"
    input_list = redis.lrange(input_key, 0, -1)
    output_list = redis.lrange(output_key, 0, -1)
    r_zipped = list(zip(input_list, output_list))
    for key, value in r_zipped:
        key = key.decode("utf-8")
        value = value.decode("utf-8")
        print("{}(*{}) -> {}".format(qualified_name, key, value))


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
