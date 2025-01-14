from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from markets.business.logging import dlog_info, dlog_warn


@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    dlog_info(user, f'Пользователь {user.phone} вошел в систему через {request.META.get('HTTP_REFERER')}')


@receiver(user_login_failed)
def log_user_login_failed(sender, credentials, request, **kwargs):
    dlog_warn(None, f'Попытка входа под именем {credentials.get('username')} через {request.META.get('HTTP_REFERER')} провалилась')


@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    dlog_info(user, f'Пользователь {user.phone} вышел из системы через {request.META.get('HTTP_REFERER')}')

