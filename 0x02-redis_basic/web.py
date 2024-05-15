#!/usr/bin/env python3
"""
Python module with tools for requesting, caching and tracking data
"""

import redis
import requests
from typing import Callable
from functools import wraps

# Initialize Redis client
redis_client = redis.Redis()


def count_requests(method: Callable) -> Callable:
    """Decorator that counts the number of requests made to a URL
    and caches their responses.
    Args:
        method (Callable): The function to be decorated."""

    @wraps(method)
    def wrapper(url):
        """wrapper function to count requests and cache responses."""
        # Increment the count for the URL
        redis_client.incr(f"count:{url}")

        # Check if the HTML content is cached
        cached_html = redis_client.get(f"cached:{url}")

        if cached_html:
            return cached_html.decode('utf-8')
        # If not cached, fetch the HTML content
        html = method(url)

        # Cache the HTML content with an expiration time of 10 seconds
        redis_client.setex(f"cached:{url}", 10, html)

        # Return the fetched HTML content
        return html

    return wrapper


def get_page(url: str) -> str:
    """Fetches HTML content of a URL and caches result with expiration.
    Args:
        url (str): The URL to fetch
    Returns:
        str: The HTML content of the URL"""

    return requests.get(url).text