from django.utils import timezone
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.urls import reverse
from product.models import Book


# Create your models here.
class DiscountCode(models.Model):
    """
    this is for invoice if have a code distinct, the code is unique and it for one order
    """
    code = models.CharField(max_length=50, unique=True)
    # valid_from = models.DateTimeField(default=timezone)
    # valid_to = models.DateTimeField(default=timezone)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    active = models.BooleanField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='code_user')

    class Meta:
        verbose_name = 'کد تخفیف'
        verbose_name_plural = 'کدهای تخفیف'

    def __str__(self):
        return self.code

    def get_absolute_url(self):
        return reverse('off:discount_detail', args=[self.pk])


class Discount(models.Model):
    """
    this is for book
    Each book can have one type of cash or percentage discount.
    """

    DISCOUNT = (('Percent', 'درصدی'), ('Cash', 'نقدی'),)
    type_discount = models.CharField(max_length=12, choices=DISCOUNT)
    amount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], blank=True, null=True)
    percent = models.DecimalField(decimal_places=2, max_digits=5, blank=True, null=True)
    max_use = models.IntegerField('Max number of items')
    active = models.BooleanField(default=True)
    book = models.ManyToManyField(Book, related_name='book_off', blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='off_user')

    class Meta:
        verbose_name = 'تخفیف'
        verbose_name_plural = 'تخفیف ها'

    def __str__(self):
        return self.type_discount

    def get_absolute_url(self):
        return reverse('off:discount_detail', args=[self.id])
