from django.urls import path
from .views import *

app_name = 'renter'

urlpatterns = [
    path('', RenterView.as_view(), name='index'),
]
