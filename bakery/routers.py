from rest_framework.routers import DefaultRouter

from accounts.viewsets import AuthViewSet

router = DefaultRouter()

router.register('accounts', AuthViewSet, basename='auth_api')