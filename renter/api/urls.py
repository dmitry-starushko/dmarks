from django.urls import path
from . import views

app_name = 'renter'

urlpatterns = [
    path('partial/calendar/<int:year>/<int:month>/', views.PV_CalendarView.as_view(), name='partial_calendar'),
]
