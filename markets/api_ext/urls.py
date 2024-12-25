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
    path('users/by-phone/<str:phone>/', views.UserCRUDView.as_view(), name='user_crud'),
    path('users/by-phone/<str:phone>/outlets/', views.UserOutletsCRUDView.as_view(), name='user_outlets_crud'),
    path('users/by-itn/<str:itn>/notifications/', views.NotificationsCRUDView.as_view(), name='user_notifications_crud'),
    path('notifications/', views.NotificationsCRUDView.as_view(), name='notifications_crud'),
]
