from django.urls import path, include
from .views import get_apartments, get_all_apartments, get_apartment_detail, redirect_to_sreality, get_filter_options

urlpatterns = [
    path('apartments/', get_apartments, name='apartment-list'),
    path('all_apartments/', get_all_apartments, name='all-apartment-list'),
    path('apartments/<str:id>/', get_apartment_detail, name='apartment-detail'),
    path('apartments/<str:id>/redirect', redirect_to_sreality, name='redirect-to-sreality'),
    path('filter-options/', get_filter_options, name='filter-options'),

    path('api-auth/', include('rest_framework.urls')),
]
