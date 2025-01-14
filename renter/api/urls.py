from django.urls import path
from markets.api.views import PV_HelpContentView
from . import views

app_name = 'renter'

urlpatterns = [
    path('partial/calendar/<int:year>/<int:month>/', views.PV_CalendarView.as_view(), name='partial_calendar'),
    path('partial/notifications/<int:year>/<int:month>/<int:day>/<int:calendar>/', views.PV_NotificationsView.as_view(), name='partial_notifications'),
    path('partial/reg-card/', views.PV_RegCardView.as_view(), name='partial_reg_card'),
    path('partial/help-content/<int:hid>/', PV_HelpContentView.as_view(), name='partial_help_content'),
    path('action/verification-data/', views.ActionVerificationDataView.as_view(), name='action_verification_data'),
    path('action/send-answer/', views.SendAnswerView.as_view(), name='send_answer'),
    path('action/download-log/', views.DownloadLogView.as_view(), name='download_log'),
]
