#!/usr/bin/env python3
"""
Python module that uses Redis NoSQL for data storage
"""

from functools import wraps
from typing import Any, Callable, Optional, Union
import uuid
import redis


def count_calls(method: Callable) -> Callable:
    """Decorator that counts the number of times a method of the
    Cache class is called"""
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ the wrapper functions """
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


class Cache:
    def __init__(self):
        """
        Initializes the Cache class and flushes the Redis instance.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[bytes, str, int, float]) -> str:
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

    def get(self, key: str, fn: Optional[Callable[[bytes], Any]] = None) -> Any:
        """
        Retrieves data from Redis using the provided key and optionally applies a conversion function.

        Args:
        key: The key used to store the data in Redis.
        fn: An optional callable function to convert the retrieved data (default: None).

        Returns:
        The retrieved data (converted if a conversion function is provided) or None if the key doesn't exist.
        """
        data = self._redis.get(key)
        if data is None:
            return None
        return fn(data) if fn else data

    def get_str(self, key: str) -> Optional[str]:
        """
        Retrieves data from Redis using the provided key and converts it
          to a string using UTF-8 decoding.

        Args:
        key: The key used to store the data in Redis.

        Returns:
        The retrieved data as a decoded string or None if the key doesn't exist.
        """
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Optional[int]:
        """
        Retrieves data from Redis using the provided key and converts it to 
        an integer.

        Args:
        key: The key used to store the data in Redis.

        Returns:
        The retrieved data as an integer or None if the key doesn't exist or
        the data cannot be converted to an integer.
        """
        return self.get(key, fn=int)