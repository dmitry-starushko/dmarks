from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from markets.models import DmUser


class DmUserCreationForm(UserCreationForm):
    class Meta:
        model = DmUser
        fields = ["first_name", "last_name", "phone", "password", "email", "is_staff", "is_active", "groups", "user_permissions"]


class DmUserChangeForm(UserChangeForm):
    class Meta:
        model = DmUser
        fields = ["first_name", "last_name", "phone", "password", "email", "is_staff", "is_active", "groups", "user_permissions"]
