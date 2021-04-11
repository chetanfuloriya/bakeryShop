from django.core.exceptions import ValidationError
from rest_framework import serializers

from product.models import BakeryItem, Ingredient


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient

        fields = '__all__'


class BakeryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BakeryItem

        fields = '__all__'

    def create(self, validated_data):
        try:
            product = BakeryItem.objects.create(**validated_data)
            return product
        except ValidationError as e:
            raise serializers.ValidationError(f'[ERROR]: {e}')
