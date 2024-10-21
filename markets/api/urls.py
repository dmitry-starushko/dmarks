from django.urls import path
from . import views

app_name = 'markets'

urlpatterns = [
    path('schemes/<int:scheme_pk>/gltf', views.TakeGltfView.as_view(), name='schemes_take_gltf'),
    path('schemes/<int:scheme_pk>/svg', views.TakeSvgView.as_view(), name='schemes_take_svg'),
    path('schemes/<int:scheme_pk>/outlets', views.TakeOutletsView.as_view(), name='schemes_take_outlets'),
]
