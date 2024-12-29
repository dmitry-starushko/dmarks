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
        return render(request, 'renter/partials/calendar.html', {})

