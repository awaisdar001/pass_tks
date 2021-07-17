"""Make external api calls here"""
import json
import sys

from api.cache import BasicCache

if sys.version_info.major < 3:
    from urllib2 import URLError, urlopen
else:
    from urllib.error import URLError
    from urllib.request import urlopen

END_POINT = 'http://api.postcodes.io'


class PostCodesAPI(BasicCache):
    """Wrapper for external postcodes api."""

    def _get_json_resp(self, uri):
        """
        Makes an API call and returns data in a data structure.

        Arguments:
             uri(string): URI to make get request to.
        Returns:
            Returns the API response or empty list.
        """
        url = f'{END_POINT}/{uri}'
        response = self.get_api_response_in_cache(uri)
        if response:
            return json.loads(response).get('result', [])

        try:
            resp = urlopen(url)
        except URLError as e:
            if e.code == 404:  # no available data
                return []
        else:
            response = resp.read()
            self.set_api_response_in_cache(uri, response)
        return json.loads(response).get('result', [])

    def get_admin_districts_or_default(self, result, default=[]):
        return result['admin_district'] if result else default

    def get_outcode(self, result):
        return result.get('outcode')

    def fetch_outcode_details(self, outcode):
        """Fetch outcode details using external api."""
        return self._get_json_resp(uri=f'outcodes/{outcode}')

    def fetch_nearest_districts_by_outcode(self, outcode):
        """Fetch nearest outcode details using external api."""
        return self._get_json_resp(uri=f'outcodes/{outcode}/nearest')

    def get_districts_by_outcode(self, outcode):
        """Returns district names that come under a outcode."""
        result = self.fetch_outcode_details(outcode)
        return self.get_admin_districts_or_default(result)

    def get_nearest_districts_by_outcode(self, outcode):
        """
        Returns the data of nearest listings by the provided outcode.

        Arguments:
             outcode(str): valid outcode
        Returns:
            Dict mapping outcode to its districts.
        """
        nearby_codes = {}
        result = self.fetch_nearest_districts_by_outcode(outcode)
        for node in result:
            outcode = self.get_outcode(node)
            admin_dist = self.get_admin_districts_or_default(node)
            if outcode:
                nearby_codes[outcode] = admin_dist
        return nearby_codes
