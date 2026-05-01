from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import redirect
from django.db.models import Q, Min, Max
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from .models import Apartment
from .serializers import ApartmentSerializer


@api_view(['GET'])
def get_apartments(request):
    apartments = Apartment.objects.filter(is_active=True)

    # Filtering
    price_min = request.query_params.get('price_min')
    price_max = request.query_params.get('price_max')
    area_min = request.query_params.get('area_min')
    area_max = request.query_params.get('area_max')
    district = request.query_params.get('district')

    # Boolean filters
    has_metro = request.query_params.get('metro')
    has_tram = request.query_params.get('tram')
    has_elevator = request.query_params.get('elevator')
    has_garage = request.query_params.get('garage')
    has_parking = request.query_params.get('parking_lots')
    furnished = request.query_params.get('furnished')
    new_building = request.query_params.get('new_building')

    # Sorting
    sort_by = request.query_params.get('sort_by', '-updated_at')

    # Price range filter
    if price_min:
        apartments = apartments.filter(price__gte=int(price_min))
    if price_max:
        apartments = apartments.filter(price__lte=int(price_max))

    # Area range filter
    if area_min:
        apartments = apartments.filter(area_m2__gte=int(area_min))
    if area_max:
        apartments = apartments.filter(area_m2__lte=int(area_max))

    # District filter
    if district:
        apartments = apartments.filter(district=int(district))

    # Boolean filters
    if has_metro == 'true':
        apartments = apartments.filter(metro=True)
    if has_tram == 'true':
        apartments = apartments.filter(tram=True)
    if has_elevator == 'true':
        apartments = apartments.filter(elevator=True)
    if has_garage == 'true':
        apartments = apartments.filter(garage=True)
    if has_parking == 'true':
        apartments = apartments.filter(parking_lots=True)
    if furnished == 'true':
        apartments = apartments.filter(Q(furnished=True) | Q(partly_furnished=True))
    if new_building == 'true':
        apartments = apartments.filter(new_building=True)

    # Sorting - validate to prevent injection
    allowed_sorts = ['price', '-price', 'area_m2', '-area_m2', 'distance_to_local_hub',
                     '-distance_to_local_hub', 'predicted_price', '-predicted_price',
                     'created_at', '-created_at', 'updated_at', '-updated_at']
    if sort_by not in allowed_sorts:
        sort_by = '-updated_at'

    apartments = apartments.order_by(sort_by)

    paginator = PageNumberPagination()
    paginator.page_size = 20

    result_page = paginator.paginate_queryset(apartments, request)
    serializer = ApartmentSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['GET'])
def get_all_apartments(request):
    apartments = Apartment.objects.order_by('-updated_at')
    serializer = ApartmentSerializer(apartments, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_apartment_detail(request, id):
    try:
        apartment = Apartment.objects.get(sreality_id=id)
    except Apartment.DoesNotExist:
        return Response(
            {"error": "Such apartment does not exist"},
            status=status.HTTP_404_NOT_FOUND
        )
    serializer = ApartmentSerializer(apartment)
    return Response(serializer.data)

@api_view(['GET'])
def redirect_to_sreality(request, id):

    try:
        apartment = Apartment.objects.get(sreality_id=id)
    except Apartment.DoesNotExist:
        return Response(
            {"error": "Such apartment does not exist"},
            status=status.HTTP_404_NOT_FOUND
        )

    sreality_id = apartment.sreality_id

    seo_locality = apartment.seo_locality


    exact_link = f"https://www.sreality.cz/detail/pronajem/byt/1+kk/{seo_locality}/{sreality_id}"
    return redirect(exact_link)


@api_view(['GET'])
def get_filter_options(_):
    """Get available options for filters"""
    apartments = Apartment.objects.filter(is_active=True)

    return Response({
        'districts': sorted(list(apartments.values_list('district', flat=True).distinct())),
        'price_range': {
            'min': apartments.aggregate(min_price=Min('price'))['min_price'],
            'max': apartments.aggregate(max_price=Max('price'))['max_price'],
        },
        'area_range': {
            'min': apartments.aggregate(min_area=Min('area_m2'))['min_area'],
            'max': apartments.aggregate(max_area=Max('area_m2'))['max_area'],
        },
        'distance_range': {
            'min': apartments.aggregate(min_dist=Min('distance_to_local_hub'))['min_dist'],
            'max': apartments.aggregate(max_dist=Max('distance_to_local_hub'))['max_dist'],
        }
    })