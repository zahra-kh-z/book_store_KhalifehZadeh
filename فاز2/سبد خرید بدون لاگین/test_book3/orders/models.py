from django.db import models
from product.models import *
from off.models import DiscountCode, Discount
from myusers.models import Address, Customer


# Create your models here.


class Invoice(models.Model):
    STATUS_CHOICES = (('Pending', 'سفارش'), ('Delivered', 'ثبت شده'))
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    # ordered = models.BooleanField(default=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    # email for order not be unique
    email = models.EmailField(unique=True, blank=True, null=True)
    # address = models.CharField(max_length=250)
    address = models.ForeignKey(Address, on_delete=models.DO_NOTHING, related_name='addr_ord', blank=True, null=True)

    # customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING, related_name='customer_ord')
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # total_price = models.BigIntegerField(null=True, blank=True)

    class Meta:
        ordering = ('-created',)  # ordering by the created field
        verbose_name = 'سبد خرید'
        verbose_name_plural = 'سبدهای خرید'

    def __str__(self):
        return f'Order {self.id}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())
        # total_cost = sum(item.get_cost() for item in self.items.all())
        # return total_cost - total_cost * (self.discount / Decimal(100))


class InvoiceItem(models.Model):
    order = models.ForeignKey(Invoice, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Book, related_name='order_items', on_delete=models.CASCADE)
    price = models.BigIntegerField(default=0)
    # price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    # ordered = models.BooleanField(default=False)
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارش ها'

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity

    def reduce_inventory(self):
        """for update inventory after buy"""
        if self.quantity > self.product.inventory:
            self.product.inventory -= self.quantity
            self.product.inventory.save()
