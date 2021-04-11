from django.contrib.auth import get_user_model
from django.core.exceptions import ImproperlyConfigured

from rest_framework.authtoken.models import Token
from rest_framework import viewsets, status
from . import serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from accounts.utils import get_and_authenticate_user


class AuthViewSet(viewsets.GenericViewSet):
    permission_classes = [AllowAny, ]
    serializer_class = serializers.EmptySerializer
    serializer_classes = {
        'login': serializers.UserLoginSerializer,
    }

    @action(methods=['POST', ], detail=False)
    def login(self, request):
        """
            : Login-API

            payload_data: {
                "email": "<email_id>",
                "password": "<xxxxxxxx>"
            }
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_and_authenticate_user(**serializer.validated_data)
        data = serializers.AuthUserSerializer(user).data
        return Response(data=data, status=status.HTTP_200_OK)

    def get_serializer_class(self):
        if not isinstance(self.serializer_classes, dict):
            raise ImproperlyConfigured("serializer_classes should be a dict mapping.")

        if self.action in self.serializer_classes.keys():
            return self.serializer_classes[self.action]
        return super().get_serializer_class()

    @action(methods=['POST', ], detail=False)
    def logout(self, request):
        """
            : Logout-API
            
            Remove all auth tokens owned by request.user.
        """
        Token.objects.filter(user=request.user).delete()
        data = {'success': 'Sucessfully logged out'}
        return Response(data=data, status=status.HTTP_200_OK)
