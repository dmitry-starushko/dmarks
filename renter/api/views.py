from calendar import monthrange

from django.http import HttpResponseBadRequest
from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from markets.decorators import on_exception_returns_response


# -- Partial views --------------------------------------------------------------------------------

class PV_CalendarView(APIView):
    permission_classes = [AllowAny]

    @on_exception_returns_response(HttpResponseBadRequest)
    def post(self, request, year: int, month: int):
        def cal_days():
            _, pds = monthrange(year, (month - 2) % 12 + 1)
            cwd, cds = monthrange(year, month)
            nds = (- cwd - cds) % 7
            pr = [i + pds - 6 for i in range(7)][-cwd:] if cwd else []
            cr = [i + 1 for i in range(cds)]
            nx = [i + 1 for i in range(nds)]
            return pr, cr, nx

        p_ds, c_ds, n_ds = cal_days()
        match request.data:
            case {'year': int(user_year), 'month': int(user_month), 'day': int(user_day)}:
                return render(request, 'renter/partials/calendar.html', {
                    'title': f'{year} {('Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь')[(month - 1) % 12]}',
                    'week_days': ('Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'),
                    'p_days': p_ds,
                    'c_days': c_ds,
                    'n_days': n_ds,
                    'today': user_day if user_year == year and user_month == month else None,
                    'events': frozenset([2, 4, 7, 12])
                })
            case _: raise ValueError(request.data)

