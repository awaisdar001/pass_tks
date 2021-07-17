import csv

from django.conf import settings


class ListingRow:
    """Helper class to encapsulate and do not expose unnecessary details for listing."""
    neighbourhood = ['']
    price = [0]

    def __init__(self, **kwargs):
        self.district = kwargs['neighbourhood_group_cleansed']
        self.daily_price = float(kwargs['price'].strip('$').replace(',', ''))


class DistrictListingReader:
    """ Class for reading listings csv file """

    def __init__(self):
        self.required_columns = ['price', 'neighbourhood_group_cleansed']
        self.file_name = settings.LISTING_FILE_NAME
        self.path = settings.STATIC_DIR / self.file_name
        self._validate()

    @property
    def _csv_reader(self):
        return csv.DictReader(open(self.path))

    def _validate(self):
        """
        Validate the data file and raises error if relevant data fields
        are not available.
        """
        field_names = self._csv_reader.fieldnames
        if not all([column in field_names for column in self.required_columns]):
            raise ValueError(
                f'Data file "{self.file_name}" is missing one of required columns: {self.required_columns}.'
            )

    def rows(self):
        """Generator for getting rows from the csv file."""
        for row in self._csv_reader:
            yield ListingRow(**row)


def sum_and_calculate_avg_for_data(dataset):
    """
    Calculates average on the dataset.
    """
    data_average = 0
    data_items = len(dataset)

    if data_items:
        data_average = round(sum(dataset) / data_items, 2)

    return data_average
