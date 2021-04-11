from django.core.exceptions import ValidationError
from django.db import models

from jsonfield import JSONField
from simple_history.models import HistoricalRecords

from base.models import TimeStampModel


class Ingredient(TimeStampModel):
    ingredient_name = models.CharField(max_length=40, null=True, blank=True)
    is_available = models.BooleanField(default=True)
    history = HistoricalRecords(history_change_reason_field=models.TextField(null=True))

    class Meta:
        verbose_name_plural = 'Ingredients'

    def __str__(self):
        """
        Returns the ingredients name when it is printed in the console
        """
        return f'{self.ingredient_name}'


class BakeryItem(TimeStampModel):
    product_name = models.CharField(max_length=40, null=True, blank=True)
    ingredients = JSONField(null=True, blank=True)
    cost_price = models.PositiveIntegerField(default=0)
    selling_price = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True)
    history = HistoricalRecords(history_change_reason_field=models.TextField(null=True))

    class Meta:
        verbose_name_plural = 'Bakery Items'

    def __str__(self):
        """
        Returns the BakeryItem name when it is printed in the console
        """
        return f'{self.product_name}'

    def save(self, *args, **kwargs):
        if not self.ingredients:
            raise ValueError('[ERROR]: Please add ingredients')

        # Get all available ingredients
        available_ingredients = Ingredient.objects.filter(
            is_available=True
        ).values_list('id', flat=True)

        # Check all added ingredients is correct or not
        for ingredient_id in self.ingredients.keys():
            if int(ingredient_id) not in available_ingredients:
                raise ValidationError(f'This ingredient({ingredient_id}) is not available for now')

        super().save(*args, **kwargs)


class HotProduct(TimeStampModel):
    product = models.OneToOneField(
        BakeryItem, null=True, blank=True, default=None, on_delete=models.PROTECT
    )
    sold_quantity = models.PositiveIntegerField(null=True, blank=True, default=0)

    class Meta:
        verbose_name_plural = 'Hot Products'

    def __str__(self):
        return f'{self.product} - {self.sold_quantity}'
