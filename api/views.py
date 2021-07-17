"""API views for listings."""
from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import ListingManager
from api.postcodes_api import PostCodesAPI
from api.utils import sum_and_calculate_avg_for_data
from pass_tks.xml_renderer import OutcodeXMLRenderer, OutcodesXMLRenderer

PostcodesAPI = PostCodesAPI()
AreaListing = ListingManager()


class OutCodeDetailView(APIView):
    """
    View for the summary for listing and avg daily rate for an outcode.
    """

    def get_renderers(self):
        """Returns the renderers that this view can use."""
        return [OutcodeXMLRenderer()]

    def get(self, request, outcode):
        """
        Returns details of listings and average daily rate for a given outcode.
        """
        outcode_districts = PostcodesAPI.get_districts_by_outcode(outcode=outcode)
        if not outcode_districts:
            raise Http404

        total_listings, average_daily_rate = AreaListing.get_avg_daily_rate_for_districts(outcode_districts)
        return Response({
            'total-listings': f'{total_listings}',
            'average-daily-rate': f'{average_daily_rate}',
            'id': f'{outcode}',
        })


class OutCodeNearestView(APIView):
    """API view for nearest districts based on outcode."""

    def get_renderers(self):
        """Returns the renderers that this view can use."""
        return [OutcodesXMLRenderer()]

    def get(self, request, outcode, **kwargs):
        """
        Returns details of nearest listings and average daily rate for a given outcode.
        """
        nearest_outcodes_prices = []
        nearest_outcodes_data = []

        nearby_districts = PostcodesAPI.get_nearest_districts_by_outcode(outcode=outcode)
        if not len(nearby_districts):
            raise Http404

        for nearby_outcode, nearby_districts in nearby_districts.items():
            daily_prices_dataset = AreaListing.get_daily_prices_for_districts(nearby_districts)
            nearest_outcodes_data.append({
                'id': f'{nearby_outcode}',
                'listing-count': f'{len(daily_prices_dataset)}',
                'average-daily-rate': f'{sum_and_calculate_avg_for_data(daily_prices_dataset)}'
            })
            nearest_outcodes_prices.extend(daily_prices_dataset)

        all_outcodes_listings = len(nearest_outcodes_prices)
        avg_dail_rate_for_outcodes = sum_and_calculate_avg_for_data(nearest_outcodes_prices)
        return Response({
            'nexus': f'{outcode}',
            'listing-count': f'{all_outcodes_listings}',
            'average-daily-rate': f'{avg_dail_rate_for_outcodes}',
            'outcodes': nearest_outcodes_data,
        })
