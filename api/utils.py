import csv

from django.conf import settings


class ListingRow:
    """Helper class to encapsulate and do not expose unnecessary details for listing."""
    district = ''
    daily_price = 0.0

    def __init__(self, **kwargs):
        self.district = kwargs['neighbourhood_group_cleansed']
        self.daily_price = float(kwargs['price'].strip('$').replace(',', ''))


def sum_and_calculate_avg_for_data(dataset):
    """
    Calculates average on the dataset.
    """
    data_average = 0
    data_items = len(dataset)

    if data_items:
        data_average = round(sum(dataset) / data_items, 2)

    return data_average
