"""Implements basic cache mechanism"""
import logging

logger = logging.getLogger(__name__)


class BasicCache:
    """Implements basic cache."""
    def __init__(self, *args, **kwargs):
        """Init and rest initial cache."""
        self._cache = {}

    def _set_cache(self, key, value):
        """Caches the provided value to the key."""
        self._cache[key] = value

    def _get_cache(self, key):
        """Returns an item in the cache."""
        return self._cache.get(key)

    def set_prices_from_cache(self, key, value):
        """Caches api prices data """
        self._set_cache(f'{key}-prices', value)

    def get_prices_from_cache(self, key):
        """Returns prices from the cache."""
        return self._get_cache(f'{key}-prices')

    def set_api_response_in_cache(self, key, value):
        """Caches api response data """
        self._set_cache(f'{key}-api', value)

    def get_api_response_in_cache(self, key):
        """Returns api response from the cache."""
        return self._get_cache(f'{key}-api')
