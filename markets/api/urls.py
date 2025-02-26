from django.urls import path
from . import views

app_name = 'markets'

urlpatterns = [
    path('schemes/<int:scheme_pk>/gltf/', views.TakeSchemeGltfView.as_view(), name='schemes_take_gltf'),
    path('schemes/<int:scheme_pk>/svg/', views.TakeSchemeSvgView.as_view(), name='schemes_take_svg'),
    path('schemes/<int:scheme_pk>/outlets/state/<int:legend>/', views.TakeSchemeOutletsStateView.as_view(), name='schemes_take_outlets_state'),
    # --
    path('info/legends/<int:legend>/', views.TakeLegendView.as_view(), name='info_take_legend'),
    path('info/path/', views.TakeURLView.as_view(), name='info_take_path'),
    path('info/urls/', views.TakeURLsView.as_view(), name='info_take_urls'),
    # --
    path('partial/outlet-table/<int:scheme_pk>/<int:legend>/', views.PV_OutletTableView.as_view(), name='partial_outlet_table'),
    path('partial/outlet-detail/<str:outlet_number>/', views.PV_OutletDetailView.as_view(), name='partial_outlet_detail'),
    path('partial/filtered-markets/', views.PV_FilteredMarketsView.as_view(), name='partial_filtered_markets'),
    path('partial/filtered-outlets/', views.PV_FilteredOutletsView.as_view(), name='partial_filtered_outlets'),
    path('partial/outlet-filters/<int:full>/', views.PV_OutletFiltersView.as_view(), name='partial_outlet_filters'),
    path('partial/legend-body/<int:legend>/', views.PV_LegendBodyView.as_view(), name='partial_legend_body'),
    path('partial/help-content/<int:hid>/', views.PV_HelpContentView.as_view(), name='partial_help_content'),
    path('partial/user-action/', views.PV_UserActionView.as_view(), name='partial_user_action'),
]
