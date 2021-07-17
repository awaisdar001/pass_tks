from django.urls import re_path

from api.views import OutCodeDetailView, OutCodeNearestView

# app_name will help us do a reverse look-up latter.
urlpatterns = [
    re_path(
        r'outcode/(?P<outcode>[A-Za-z0-9]{2,4})/$',
        OutCodeDetailView.as_view(),
        name='detail'
    ),
    re_path(
        r'nexus/(?P<outcode>[A-Za-z0-9]{2,4})/$',
        OutCodeNearestView.as_view(),
        name='detail'
    ),
]
