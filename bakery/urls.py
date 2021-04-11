from django.contrib import admin
from django.urls import include, path
from bakery.routers import router

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/accounts/', include('accounts.urls')),
    path('api/v1/product/', include('product.urls')),
    path('api/v1/', include(router.urls))
]
