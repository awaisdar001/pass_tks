"""Data models for the api app."""
from api.cache import BasicCache
from api.listing_reader import DistrictListingReader
from api.utils import sum_and_calculate_avg_for_data


class ListingManager(BasicCache):
    """Data model for listings that using basic cache mechanism."""

    def __init__(self, *args, **kwargs):
        self.listing_reader = DistrictListingReader()
        super().__init__(*args, **kwargs)

    def get_district_prices(self, district):
        """
        Returns all listings daily prices for a district.

        Arguments:
            district(str): name of the district.
        """
        cache_hit = self.get_prices_from_cache(district)
        if cache_hit:
            return cache_hit

        prices = []

        def district_rows(stream):
            """Filters and matches rows that match with provided district."""
            for row in stream:
                if row.district == district:
                    yield row

        for listing in district_rows(self.listing_reader.rows()):
            prices.append(listing.daily_price)

        self.set_prices_from_cache(district, prices)
        return prices

    def get_daily_prices_for_districts(self, districts):
        """Returns all listings daily prices for provided districts."""
        all_prices = []

        for district_name in districts:
            prices = self.get_district_prices(district_name)
            all_prices.extend(prices)
        return all_prices

    def get_avg_daily_rate_for_districts(self, districts):
        """
        Returns total listings and avg daily rate for given district names.

        Arguments:
            districts (list): List of district names.
        """
        all_prices = self.get_daily_prices_for_districts(districts)
        total_listings = len(all_prices)
        average_daily_rate = sum_and_calculate_avg_for_data(all_prices)
        return total_listings, average_daily_rate
