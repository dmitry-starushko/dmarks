from django.utils.safestring import mark_safe
from markets.models import Parameter


def parameters_processor(_):
    return {
        f'parm_{p.key}': mark_safe(p.value) for p in Parameter.objects.filter(preload=True)
    }
