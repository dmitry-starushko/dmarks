from django.urls import path
from django.contrib.auth import views as auth_views
from .api.views import LogoutView
from .views import *

app_name = 'renter'

urlpatterns = [
    path('', RenterView.as_view(), name='renter'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
