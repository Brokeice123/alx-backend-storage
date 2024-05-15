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


def call_history(method: Callable) -> Callable:
    """
    Decorator that stores call history (inputs and outputs) for a function.

    Args:
        method: The method to be decorated (Callable).

    Returns:
        A callable that wraps the original method and stores call history.
    """
    input_list = method.__qualname__ + ":inputs"
    output_list = method.__qualname__ + ":outputs"

    @wraps(method)
    def wrapper(self, *args) -> bytes:
        """
        Wrapper function that stores call history and executes the
        decorated function.

        Args:
            self: The instance of the Cache class.
            *args: Arguments passed to the original method.

        Returns:
            The return value of the original method.
        """
        input = str(args)
        self._redis.rpush(input_list, input)
        output = method(self, *args)
        self._redis.rpush(output_list, output)
        return output
    return wrapper


def replay(method: Callable) -> None:
    """
    Displays the call history for a decorated function.
    """
    cache = redis.Redis()
    name = method.__qualname__

    calls = cache.get(name).decode("utf-8")

    print(f"{name} was called {calls} times:")

    inputs = cache.lrange(name + ":inputs", 0, -1)
    outputs = cache.lrange(name + ":outputs", 0, -1)

    for i, out in zip(inputs, outputs):
        print("{}(*{}) -> {}"
              .format(name, i.decode('utf-8'), out.decode('utf-8')))


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

    def get(self, key: str,
            fn: Optional[Callable[[bytes], Any]] = None) -> Any:
        """
        Retrieves data from Redis using the provided key and optionally applies
        a conversion function.

        Args:
        key: The key used to store the data in Redis.
        fn: An optional callable function to convert the retrieved data
        (default: None).

        Returns:
        The retrieved data (converted if a conversion function is provided)
        or None if the key doesn't exist.
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
        The retrieved data as a decoded string or None if the key doesn't
        exist.
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
