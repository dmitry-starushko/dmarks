from django.http import HttpResponseBadRequest
from rest_framework.fields import IntegerField
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from markets.api.serializers import TradePlaceSerializer
from markets.business.search_and_filters import apply_filter
from markets.decorators import on_exception_returns_response
from markets.models import TradePlace, SvgSchema


class TradePlaceSerializerO(TradePlaceSerializer):
    legend_id = IntegerField(source='trade_place_type_id')

    class Meta:
        model = TradePlace
        fields = TradePlaceSerializer.Meta.fields + ['legend_id']


class TradePlaceSerializerS(TradePlaceSerializer):
    legend_id = IntegerField(source='trade_spec_type_id_act_id')

    class Meta:
        model = TradePlace
        fields = TradePlaceSerializer.Meta.fields + ['legend_id']


class TradePlaceSerializerSec(TradePlaceSerializer):
    legend_id = IntegerField(source='location_sector_id')

    class Meta:
        model = TradePlace
        fields = TradePlaceSerializer.Meta.fields + ['legend_id']


class TakeSchemeOutletsListView(ListAPIView):
    permission_classes = [AllowAny]
    legends = [TradePlaceSerializerO, TradePlaceSerializerS, TradePlaceSerializerSec]

    @on_exception_returns_response(HttpResponseBadRequest)
    def post(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        scheme_pk = int(self.kwargs['scheme_pk'])
        scheme = SvgSchema.objects.get(pk=scheme_pk)
        queryset = scheme.outlets.all()
        if self.request.data:
            for f_name, f_body in self.request.data.items():
                queryset = apply_filter(queryset, f_name, f_body)
        return queryset

    def get_serializer_class(self):
        legend = int(self.kwargs['legend']) % len(self.legends)
        return self.legends[legend]
