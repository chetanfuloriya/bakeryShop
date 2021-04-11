from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from product.models import BakeryItem, HotProduct, Ingredient


@admin.register(Ingredient)
class IngredientAdmin(SimpleHistoryAdmin):
    list_display = ('id', 'ingredient_name', 'is_available',)
    search_fields = ('ingredient_name',)
    readonly_fields = ('created_at', 'modified_at')
    list_filter = ('is_available',)


@admin.register(BakeryItem)
class BakeryItemAdmin(SimpleHistoryAdmin):
    list_display = ('id', 'product_name', 'is_available', 'cost_price', 'selling_price')
    search_fields = ('product_name',)
    readonly_fields = ('created_at', 'modified_at')
    list_filter = ('is_available',)


@admin.register(HotProduct)
class HotProductAdmin(SimpleHistoryAdmin):
    list_display = ('product', 'sold_quantity',)
    search_fields = ('product__id',)
    readonly_fields = ('created_at', 'modified_at')
    raw_id_fields = ('product',)
