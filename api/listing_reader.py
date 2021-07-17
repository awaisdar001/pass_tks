"""Logic for reading datafile goes here."""

from csv import DictReader

from django.conf import settings

from api.utils import ListingRow


class DistrictListingReader:
    """ Class for reading listings csv file """

    def __init__(self):
        self.required_columns = settings.LISTING_REQUIRED_DATA_COLS
        self.file_name = settings.LISTING_FILE_NAME
        self.file_path = settings.STATIC_DIR / self.file_name
        self._validate()

    @property
    def _csv_reader(self):
        return DictReader(open(self.file_path))

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
