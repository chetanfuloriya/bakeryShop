from django.urls import path

from product.services import AddIngredients, BakeryProducts, FetchBakeryProducts, TopSellingProducts

urlpatterns = [
    path('add_ingredients/', AddIngredients.as_view(), name='add_ingredients'),
    path('add_product/', BakeryProducts.as_view(), name='add_product'),
    path('get_product_detail/', BakeryProducts.as_view(), name='get_product_detail'),
    path('fetch_products/', FetchBakeryProducts.as_view(), name='fetch_products'),
    path('top_selling_products/', TopSellingProducts.as_view(), name='top_selling_products')
]
