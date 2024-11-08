from collections import OrderedDict
from django.utils.safestring import mark_safe
from markets.models import Parameter, TradePlaceType


def parameters_processor(_):
    return {
        f'parm_{p.key}': mark_safe(p.value) for p in Parameter.objects.filter(preload=True)
    }


def outlet_states_processor(_):
    states = OrderedDict()
    for tpt in TradePlaceType.objects.all():
        states[tpt.id] = {
            'title': tpt.type_name,
            'wall_color': mark_safe(tpt.wall_color),
            'roof_color': mark_safe(tpt.roof_color),
            'wall_color_css': mark_safe(f'#{hex(int(tpt.wall_color, 16))[2:]}'),
            'roof_color_css': mark_safe(f'#{hex(int(tpt.roof_color, 16))[2:]}'),
        }
    return {
        'legend': states
    }
