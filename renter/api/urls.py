from django.urls import path
from . import views

app_name = 'renter'

urlpatterns = [
    path('partial/calendar/<int:year>/<int:month>/', views.PV_CalendarView.as_view(), name='partial_calendar'),
    path('partial/notifications/<int:year>/<int:month>/<int:day>/<int:calendar>/', views.PV_NotificationsView.as_view(), name='partial_notifications'),
    path('partial/reg-card/', views.PV_RegCardView.as_view(), name='partial_reg_card'),
    path('action/verification/data/', views.FormActionVerificationDataView.as_view(), name='action_verification_data'),
]
