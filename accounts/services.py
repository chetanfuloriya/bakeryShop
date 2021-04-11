from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.http.request import QueryDict

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from accounts.models import Order
from accounts.serializers import OrderSerializer, RegisterSerializer

User = get_user_model()


class Register(generics.CreateAPIView):
    """
    : Register-API

    Payload_data: {
        "email": "<email_id>",
        "password": "<xxxxxxxx>",
        "password2": "<xxxxxxx>",
        "first_name": "<first_name>",
        "last_name": "<last_name>",
        "mobile": "<xxxxxxxxxx>"
    }
    """
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class PlaceOrder(APIView):
    def get(self, request):
        """
            : GET_API
            Fetch Order history.
        """
        # Restrict Anonymous user.
        if not isinstance(self.request.user, User):
            msg = '[ERROR]: Please login to check order history.'
            return Response(msg, status=400)

        all_orders = Order.objects.filter(user=self.request.user).order_by('-modified_at')

        serializer = OrderSerializer(all_orders, many=True)

        return Response(serializer.data, status=200)

    def post(self, request):
        """
            : POST_API
            Place Order

            Payload_data: {
                "product_details": {
                    "<product_id>": <no. of quantity>,
                }
            }
        """
        data = self.request.data
        user = self.request.user
        product_details = data.get('product_details')

        # Restrict Anonymous user.
        if not isinstance(user, User):
            msg = '[ERROR]: Please login to place an order.'
            return Response(msg, status=400)

        try:
            if isinstance(data, QueryDict):
                # Setting the QueryDict as mutable otherwise the
                # operations being done below won't be possible.
                data._mutable = True

            data.update({'user': user.pk})

        except Exception:
            msg = '[ERROR]: Unable to process your order at the moment.'
            return Response(msg, status=400)

        if not product_details:
            msg = '[ERROR]: Please add atleast one product.'
            return Response(msg, status=400)

        serializer = OrderSerializer(data=data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response(serializer.data, status=201)
