from django.urls import path
from . import views

app_name = 'markets'

urlpatterns = [
    path('markets/<str:mid>/', views.MarketCRUDView.as_view(), name='market_crud'),
    path('markets/<str:mid>/outlets/', views.MarketOutletsCRUDView.as_view(), name='market_outlets_crud'),
    path('markets/<str:mid>/schemes/', views.MarketSchemesCRUDView.as_view(), name='market_schemes_crud'),
    path('markets/<str:mid>/images/', views.MarketImagesCRUDView.as_view(), name='market_images_crud'),
    path('markets/<str:mid>/phones/', views.MarketPhonesCRUDView.as_view(), name='market_phones_crud'),
    path('markets/<str:mid>/emails/', views.MarketEmailsCRUDView.as_view(), name='market_emails_crud'),
    # --
    path('users/<str:itn>/confirmed/', views.UserConfirmedView.as_view(), name='user_confirmed'),
    path('users/<str:itn>/rented-outlets/', views.UserRentedOutletsView.as_view(), name='user_rented_outlets'),
    path('users/<str:itn>/notifications/', views.NotificationsCRUDView.as_view(), name='user_notifications_crud'),
    path('notifications/', views.NotificationsCRUDView.as_view(), name='notifications_crud'),
]
