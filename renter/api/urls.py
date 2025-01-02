from django.urls import path
from . import views

app_name = 'renter'

urlpatterns = [
    path('partial/calendar/<int:year>/<int:month>/', views.PV_CalendarView.as_view(), name='partial_calendar'),
    path('partial/notifications/<int:year>/<int:month>/<int:day>/<int:calendar>/', views.PV_NotificationsView.as_view(), name='partial_notifications'),
    path('partial/verification/', views.PV_VerificationView.as_view(), name='partial_verification'),
]
