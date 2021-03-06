from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
import uuid


# from django_extensions.db.fields import AutoSlugField

# Create your models here.
class Category(models.Model):
    """type category for books"""
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cat_user')

    class Meta:
        ordering = ('name',)
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product:product_list_by_category', args=[self.slug])


class Book(models.Model):
    """for register feature of book"""
    LABEL = (('New', 'جدید'), ('BestSeller', 'پرفروش'))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='book_user')
    label = models.CharField(choices=LABEL, max_length=12)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, blank=True, null=True)
    author = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    price = models.BigIntegerField(default=0)
    unit_price = models.BigIntegerField(default=0)
    category = models.ManyToManyField(Category, related_name='books_cat')
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    available = models.BooleanField(default=True)
    discount_book = models.FloatField(blank=True, null=True, default=0)
    inventory = models.IntegerField(default=0)
    can_backorder = models.BooleanField(default=False)

    # id = models.UUIDField(primary_key=True, db_index=True, default=uuid.uuid4, editable=False)
    # discount = models.ManyToManyField(Discount, related_name='book_off', blank=True, null=True, default=0)
    # slug = AutoSlugField(null=True, default=None, unique=True, populate_from='name', db_index=True)

    class Meta:
        verbose_name = 'کتاب'
        verbose_name_plural = 'کتاب ها'
        ordering = ["label", "-created"]
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """for save slug automatic"""
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('product:product_detail', args=[self.id, self.slug])

    @property
    def can_order(self):
        if self.has_inventory():
            return True
        elif self.can_backorder:
            return True
        return False

    @property
    def order_btn_title(self):
        if self.can_order and not self.has_inventory():
            return "Backorder"
        if not self.can_order:
            # موجودی انبار کافی نیست
            return f"Can not purchase. inventory is {self.inventory}"
        return "Purchase"

    def has_inventory(self):
        if self.inventory > 0:
            a = self.inventory
        return self.inventory > 0  # True or False

    def remove_items_from_inventory(self, count=1, save=True):
        current_inv = self.inventory
        if self.inventory > 0:
            current_inv -= count
            self.inventory = current_inv
        if save == True:
            self.save()
        return self.inventory


class Inventory(models.Model):
    """for num of book in inventory"""

    class Meta:
        verbose_name = 'موجودی'
        verbose_name_plural = 'موجودی ها'
        ordering = ["count_use"]

    book = models.ForeignKey(Book, on_delete=models.DO_NOTHING, related_name='books_inv')
    count_use = models.IntegerField(default=0)
    cont_new = models.IntegerField(default=1)

    def has_inventory(self):
        return self.cont_new > 0  # True or False

    @property
    def can_order(self):
        if self.has_inventory():
            return True
        return False

    def __str__(self):
        return self.book.name + ': ' + str(self.cont_new)

    def check_inventory(self, quantity):

        if quantity > self.cont_new:
            # go to set address
            self.reduce_inventory(quantity)
        else:
            print('inventory is empty')

    def add_inventory(self, num):
        """for update inventory by staff"""
        self.cont_new += num
        self.save()

    def reduce_inventory(self, quantity):
        """for update inventory after buy"""
        if quantity > self.cont_new:
            self.cont_new -= quantity
            self.save()
        else:
            print('inventory is empty')

    def is_best_sale(self):
        if self.count_use > 20:
            return True
        else:
            return False
