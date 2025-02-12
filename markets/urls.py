from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from .views import *

app_name = 'markets'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('<int:mpk>', IndexView.as_view(), name='index_mpk'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('market-detail/<int:mpk>/<str:show>/', MarketDetailsView.as_view(), name='market_details'),
    path('market-detail/<int:mpk>/<str:show>/<str:outlet>/', MarketDetailsView.as_view(), name='market_details_outlet'),
    # --- API documenting ---
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='markets:schema'), name='docs'),
]
