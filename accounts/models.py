from django.core.exceptions import ValidationError
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from jsonfield import JSONField
from simple_history.models import HistoricalRecords

from base.models import TimeStampModel
from product.models import BakeryItem, HotProduct
from accounts.managers import UserManager


class UserTypes:
    ADMIN = 1
    CUSTOMER = 2


class User(AbstractBaseUser, PermissionsMixin, TimeStampModel):
    USER_TYPE_CHOICES = (
        (None, 'Please select a user type.'),
        (UserTypes.ADMIN, 'Admin'),
        (UserTypes.CUSTOMER, 'Customer'),
    )

    first_name = models.CharField(max_length=128, blank=True, null=True, default='')
    last_name = models.CharField(max_length=128, blank=True, null=True, default='')
    email = models.EmailField(max_length=256, blank=True, null=True, unique=True)
    mobile = models.CharField(max_length=10, blank=True, null=True, unique=True)
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    history = HistoricalRecords(history_change_reason_field=models.TextField(null=True))

    objects = UserManager()

    # Email address to be used as the username
    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name_plural = 'Users'

    def __str__(self):
        """
        Returns the email of the User when it is printed in the console
        """
        return f'{self.email}'

    def get_full_name(self):
        """
        Returns the full name of the user.
        """
        full_name = self.first_name

        if self.middle_name:
            full_name = f'{full_name} {self.middle_name}'
        if self.last_name:
            full_name = f'{full_name} {self.last_name}'

        return full_name

    def save(self, *args, **kwargs):
        if self.email:
            if '@bakery' not in self.email:
                self.user_type = UserTypes.CUSTOMER
            else:
                self.user_type = UserTypes.ADMIN

        super().save(*args, **kwargs)


class CouponTypes:
    OVER_500_SHOPPING = 1
    UNDER_500_SHOPPING = 2


class Order(TimeStampModel):
    COUPON_TYPE_CHOICES = (
        (None, 'Please select a coupon type.'),
        (CouponTypes.OVER_500_SHOPPING, 'Over 500 Shopping'),
        (CouponTypes.UNDER_500_SHOPPING, 'Under 500 Shopping'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='orders'
    )
    product_details = JSONField(null=True, blank=True)
    actual_price = models.PositiveIntegerField(default=0)
    price_after_discount = models.PositiveIntegerField(null=True, blank=True, default=0)
    coupon_applied = models.PositiveSmallIntegerField(choices=COUPON_TYPE_CHOICES, blank=True, null=True)
    discount = models.PositiveIntegerField(null=True, blank=True, default=0)
    history = HistoricalRecords(history_change_reason_field=models.TextField(null=True))

    class Meta:
        verbose_name_plural = 'Orders'

    def __str__(self):
        """
        Returns the order_id of the User when it is printed in the console
        """
        return f'{self.user.email} - {self.id}'

    def save(self, *args, **kwargs):
        if not self.product_details:
            raise ValidationError('[ERROR]: Please add atleast one product.')

        for product_id, quantity in self.product_details.items():
            # Caluclating total bill of the order.
            try:
                product = BakeryItem.objects.get(id=product_id)
                self.actual_price += product.selling_price * quantity

                # Keeping track of the sold product count.
                try:
                    hot_product = HotProduct.objects.get(product=product)
                    hot_product.sold_quantity += quantity
                    hot_product.save()
                except HotProduct.DoesNotExist:
                    HotProduct.objects.create(product=product, sold_quantity=quantity)
            except BakeryItem.DoesNotExist:
                continue

        # If total bill amount is greater than `Rs.500` then
        # give flat `10%` discount.
        if self.coupon_applied == CouponTypes.OVER_500_SHOPPING:
            if self.actual_price > 500:
                self.price_after_discount = self.actual_price * 0.9
                self.discount = 10
            else:
                raise ValidationError(
                    'This coupon cannot be applied under rs.500 shopping. Please add more products.'
                )

        # This coupon can be applied for any amount and
        # give flat `5%` discount.
        elif self.coupon_applied == CouponTypes.UNDER_500_SHOPPING:
            self.price_after_discount = self.actual_price * 0.95
            self.discount = 5

        super().save(*args, **kwargs)
