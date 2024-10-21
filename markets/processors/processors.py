from django.utils.safestring import mark_safe
from markets.models import Parameter, TradePlaceType


def parameters_processor(_):
    return {
        f'parm_{p.key}': mark_safe(p.value) for p in Parameter.objects.filter(preload=True)
    }


def outlet_states_processor(_):
    states = dict()
    for tpt in TradePlaceType.objects.all():
        states[tpt.id] = {
            'title': tpt.type_name,
            'color': tpt.color or '#ffffff',
            'wall_color': tpt.wall_color,
            'roof_color': tpt.roof_color
        }
    return {
        'outlet_states': states
    }
