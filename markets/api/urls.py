from django.urls import path
from . import views

app_name = 'markets'

urlpatterns = [
    path('markets/<int:market_pk>/schemes/list', views.TakeMarketSchemesListView.as_view(), name='markets_take_schemes'),
    # --
    path('schemes/<int:scheme_pk>/gltf', views.TakeSchemeGltfView.as_view(), name='schemes_take_gltf'),
    path('schemes/<int:scheme_pk>/svg', views.TakeSchemeSvgView.as_view(), name='schemes_take_svg'),
    path('schemes/<int:scheme_pk>/outlets/state/<int:legend>', views.TakeSchemeOutletsStateView.as_view(), name='schemes_take_outlets_state'),
    path('schemes/<int:scheme_pk>/outlets/list/<int:legend>', views.TakeSchemeOutletsListView.as_view(), name='schemes_take_outlets_list'),
    # --
    path('info/legends/<int:legend>', views.TakeLegendView.as_view(), name='info_take_legend'),
    path('info/urls', views.TakeURLsView.as_view(), name='info_take_urls'),
    # --
    path('run/restore-db-consistency', views.RestoreDatabaseConsistencyView.as_view(), name='run_restore_db_consistency'),
]
