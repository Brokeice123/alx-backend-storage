#!/usr/bin/env python3
"""
Python module that uses Redis NoSQL for data storage
"""

import uuid
import redis


class Cache:
    def __init__(self):
        """
        Initializes the Cache class and flushes the Redis instance.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: bytes | str | int | float) -> str:
        """
        Stores the provided data in Redis and returns the generated key.

        Args:
            data: The data to be cached (can be bytes, string,
            integer, or float).

        Returns:
            str: The randomly generated key used to store the data.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
