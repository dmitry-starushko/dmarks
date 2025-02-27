from django.conf import settings
from django.utils.safestring import mark_safe
from markets.models import Parameter


def parameters_processor(request):
    return {
        f'parm_{p.key}': mark_safe(p.value) for p in Parameter.objects.filter(preload=True)
    } | {
        'site_root': settings.SITE_ROOT,
        'absolute_uri': f'{settings.SITE_ROOT}{request.path}'
    }
