import datetime
from calendar import monthrange
from io import BytesIO
from django.contrib.auth import logout
from django.db import transaction
from django.http import HttpResponseBadRequest, FileResponse
from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_encode
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from markets.business.confirmation import init_confirmation, ConfirmationError
from markets.business.aux_info import get_reg_card
from markets.business.logging import dlog_info
from markets.decorators import on_exception_returns_response
from markets.models import Notification, AuxUserData, File
from markets.tasks import st_deliver_answer
from renter.forms.verification import VerificationForm


# -- Partial views --------------------------------------------------------------------------------

class PV_CalendarView(APIView):
    permission_classes = [IsAuthenticated]

    @on_exception_returns_response(HttpResponseBadRequest)
    def post(self, request, year: int, month: int):
        cwd, cdn = monthrange(year, month)

        def cal_days():
            _, pdn = monthrange(year, (month - 2) % 12 + 1)
            ndn = (- cwd - cdn) % 7
            pr = [i + pdn - 6 for i in range(7)][-cwd:] if cwd else []
            cr = [i + 1 for i in range(cdn)]
            nx = [i + 1 for i in range(ndn)]
            return pr, cr, nx

        match request.data:
            case {'year': int(user_year), 'month': int(user_month), 'day': int(user_day)}:
                p_ds, c_ds, n_ds = cal_days()
                date_first = f'{year}-{month}-1'
                date_last = f'{year}-{month}-{cdn}'
                events = Notification.objects.filter(user__isnull=True, calendar_event=True, published__lte=date_last, unpublished__gt=date_first)
                if hasattr(request.user, 'notifications'):
                    events |= request.user.notifications.filter(calendar_event=True, published__lte=date_last, unpublished__gt=date_first)
                c_ds = {d: {'class': set(), 'click': False} for d in c_ds}
                if user_year == year and user_month == month and user_day in c_ds:
                    c_ds[user_day]['class'].add('today')
                for d, v in c_ds.items():
                    for event in events:
                        if event.published <= datetime.date(year, month, d) < event.unpublished:
                            v['class'].add('events')
                            v['click'] = True
                            break
                for d, v in c_ds.items():
                    v['class'] = ' '.join(v['class'])
                    if v['click']:
                        v['click'] = {'year': year, 'month': month, 'day': d}
                return render(request, 'renter/partials/calendar.html', {
                    'title': f'{year} {('Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь')[(month - 1) % 12]}',
                    'week_days': ('Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'),
                    'p_days': p_ds,
                    'c_days': c_ds,
                    'n_days': n_ds
                })
            case _: raise ValueError(request.data)


class PV_NotificationsView(APIView):
    permission_classes = [IsAuthenticated]

    @on_exception_returns_response(HttpResponseBadRequest)
    def post(self, request, year: int, month: int, day: int, calendar: int):
        date = f'{year}-{month}-{day}'
        calendar = bool(calendar)
        notifications = Notification.objects.filter(user__isnull=True, calendar_event=calendar, published__lte=date, unpublished__gt=date)
        if hasattr(request.user, 'notifications'):
            notifications |= request.user.notifications.filter(calendar_event=calendar, published__lte=date, unpublished__gt=date)
        response = render(request, 'renter/partials/notifications.html', {
            'year': year,
            'month': month,
            'day': day,
            'notifications': notifications
        })
        for ntf in notifications:
            if ntf.user is not None:
                ntf.read = True
                ntf.save()
        return response


class PV_RegCardView(APIView):
    permission_classes = [IsAuthenticated]

    @on_exception_returns_response(HttpResponseBadRequest)
    def post(self, request):
        user = request.user
        context = {'user': user, 'reg_card': get_reg_card(user)}
        if not hasattr(user, 'aux_data'):
            context |= {'form': VerificationForm()}
        return render(request, 'renter/partials/reg-card.html', context)


class ActionVerificationDataView(APIView):
    permission_classes = [IsAuthenticated]

    @on_exception_returns_response(HttpResponseBadRequest)
    def post(self, request):
        form = VerificationForm(request.POST, request.FILES)
        if form.is_valid():
            ule = request.FILES['usr_le_extract']
            # pim = request.FILES['passport_scan']
            response = redirect('renter:renter')
            with transaction.atomic():
                aux_data = AuxUserData.objects.create(
                    user=request.user,
                    itn=form.cleaned_data['itn'],
                    usr_le_extract=File.objects.create(file_name=ule.name, file_content=ule.read()),
                    # passport_image=File.objects.create(file_name=pim.name, file_content=pim.read())
                )
                try:
                    init_confirmation(request.user)
                except ConfirmationError:
                    aux_data.delete()
                    response['Location'] += f'?message={urlsafe_base64_encode('Произошла ошибка обращения к серверу. Данные не были отправлены!'.encode('utf-8'))}'
            return response
        raise RuntimeError('Ошибка в данных')


class DownloadLogView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        content = BytesIO()
        for r in request.user.log_records.order_by('-created_at'):
            content.write(f'{r.created_at_mt} | {r.kind:8} | {r.text}\n'.encode())
        content.seek(0)
        response = FileResponse(content)
        response['Content-Type'] = 'application/x-binary'
        response['Content-Disposition'] = f'attachment; filename="log{request.user.phone}-{datetime.datetime.now()}.txt"'
        return response


class SendAnswerView(APIView):
    permission_classes = [IsAuthenticated]

    @on_exception_returns_response(HttpResponseBadRequest)
    def post(self, request):
        user = request.user
        data = request.data
        match data:
            case {'question_uuid': str(uuid), 'answer': bool(answer)}:
                ntf = user.notifications.get(question_uuid=uuid)
                st_deliver_answer.delay(user.itn, uuid, answer)
                yes_no = f'«{'Да' if answer else 'Нет'}»'
                ntf.text += f'\n\n_```Вы ответили: {yes_no}```_'
                ntf.question_uuid = None
                ntf.save()
                dlog_info(user, f'Пользователь {user.phone} ответил {yes_no} на вопрос {uuid}')
            case _: raise ValueError(data)
        return Response({'result': True})


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    @on_exception_returns_response(HttpResponseBadRequest)
    def post(self, request):
        logout(request)
        return redirect('markets:index')
