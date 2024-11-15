from django.urls import path
from . import views

app_name = 'markets'

urlpatterns = [
    path('outlets/<str:location_number>', views.GetOutletView.as_view(), name='outlets_take_by_number'),
]
