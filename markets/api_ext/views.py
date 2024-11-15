from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny
from markets.models import TradePlace
from .serializers import TradePlaceSerializer


# -- EXT API --


class GetOutletView(RetrieveAPIView):
    permission_classes = [AllowAny]
    queryset = TradePlace.objects.all()
    serializer_class = TradePlaceSerializer
    lookup_field = 'location_number'
