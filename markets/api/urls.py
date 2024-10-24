from django.urls import path
from . import views

app_name = 'markets'

urlpatterns = [
    path('schemes/<int:scheme_pk>/gltf', views.TakeGltfView.as_view(), name='schemes_take_gltf'),
]
