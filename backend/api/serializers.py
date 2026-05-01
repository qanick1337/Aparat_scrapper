from rest_framework import serializers
from .models import Apartment

class ApartmentSerializer(serializers.ModelSerializer):
    price_diff = serializers.SerializerMethodField(method_name= 'get_price_diff')

    class Meta:
        model = Apartment
        fields = '__all__'

    def get_price_diff(self, obj):
        if obj.predicted_price:
            # Greater than 0 ( > 0) = Good deal
            # Lower than 0 ( < 0) = Too much
            return obj.predicted_price - obj.price
        return None