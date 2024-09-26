from django.urls import path
from .views import *

app_name = 'markets'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('pure/', PureView.as_view(), name='pure'),
]