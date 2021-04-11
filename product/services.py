from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.permissions import has_permission
from product.models import BakeryItem, HotProduct
from product.serializers import BakeryItemSerializer, IngredientSerializer

User = get_user_model()


class AddIngredients(APIView):
    def post(self, request):
        """
        : POST_API
        To add an ingredient.

        Payload_data: {
            "ingredient_name": "<ingredient_name>"
        }
        """
        data = self.request.data
        user = self.request.user

        # Check user accessibility
        if not has_permission(user):
            msg = '[ERROR]: You do not have right to add ingredients'
            return Response(msg, status=403)

        serializer = IngredientSerializer(data=data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response(serializer.data, status=201)


class BakeryProducts(APIView):
    def get(self, request):
        """
        : GET_API
        Get bakery item detail.

        Payload_data: {
            "product_id": "<product_id>"
        }
        """
        user = self.request.user

        # Check user accessibility
        if not has_permission(user):
            msg = '[ERROR]: You do not have right to get product details.'
            return Response(msg, status=403)

        product_id = self.request.data.get('product_id')

        # Get bakery_item detail for which request comes.
        try:
            bakery_item = BakeryItem.objects.get(id=product_id)
        except BakeryItem.DoesNotExist:
            msg = '[ERROR]: Product does not exist for this id.'
            return Response(msg, status=403)

        serializer = BakeryItemSerializer(bakery_item)

        return Response(serializer.data, status=200)

    def post(self, request):
        """
        : POST_API
        Add bakery items

        Payload_data: {
            "product_name": "<product_name>",
            "ingredients": {
                "<ingredient_id>": "<ingredient>%",
                "<ingredient_id>": "<ingredient>%",
                "<ingredient_id>": "<ingredient>%"
            },
            "cost_price": <cost_price>,
            "selling_price": <selling_price>
        }
        """
        data = self.request.data
        user = self.request.user

        # Check user accessibility
        if not has_permission(user):
            msg = '[ERROR]: You do not have right to add products in bakery.'
            return Response(msg, status=403)

        serializer = BakeryItemSerializer(data=data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response(serializer.data, status=201)


class FetchBakeryProducts(APIView):
    def get(self, request):
        """
            : GET_API
            Get bakery products
        """
        # List of all availble bakery items.
        all_products = BakeryItem.objects.filter(is_available=True)
        serializer = BakeryItemSerializer(all_products, many=True)

        return Response(serializer.data, status=200)


class TopSellingProducts(APIView):
    def get(self, request):
        """
            : GET_API
            Get top 3 most selling products
        """
        top_selling_product_id = HotProduct.objects.values_list(
            'product_id', flat=True
        ).order_by('-sold_quantity')[:3]

        top_selling_products = BakeryItem.objects.filter(id__in=top_selling_product_id)

        serializer = BakeryItemSerializer(top_selling_products, many=True)

        return Response(serializer.data, status=200)
