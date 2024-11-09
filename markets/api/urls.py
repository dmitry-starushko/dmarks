from django.urls import path
from . import views

app_name = 'markets'

urlpatterns = [
    path('markets/<int:market_pk>/schemes/list', views.TakeMarketSchemesListView.as_view(), name='markets_take_schemes'),
    # --
    path('schemes/<int:scheme_pk>/gltf', views.TakeSchemeGltfView.as_view(), name='schemes_take_gltf'),
    path('schemes/<int:scheme_pk>/svg', views.TakeSchemeSvgView.as_view(), name='schemes_take_svg'),
    path('schemes/<int:scheme_pk>/outlets/state', views.TakeSchemeOutletsStateView.as_view(), name='schemes_take_outlets_state'),
    path('schemes/<int:scheme_pk>/outlets/list', views.TakeSchemeOutletsListView.as_view(), name='schemes_take_outlets_list'),
    # --
    path('run/restore-db-consistency', views.RestoreDatabaseConsistencyView.as_view(), name='run_restore_db_consistency'),
]
