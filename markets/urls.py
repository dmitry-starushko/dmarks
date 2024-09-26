from django.urls import path
from .views import *

app_name = 'markets'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
]