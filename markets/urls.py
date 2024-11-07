from django.urls import path
from .views import *

app_name = 'markets'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('market-details/<int:mpk>/<str:show>/', MarketDetailsView.as_view(), name='market_details'),
    path('test/<int:scheme_pk>/', Scheme3DView.as_view(), name='test_scheme_3d_view'),
    #  Partials
    path('partials/outlet-details/<str:outlet_number>/', OutletDetailsPartialView.as_view(), name='partials_outlet_details'),
]