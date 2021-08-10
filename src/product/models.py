from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid


# Create your models here.
class Category(models.Model):
    """type category for books"""

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'

    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Book(models.Model):
    """for register feature of book"""
    LABEL = (('New', 'جدید'), ('BestSeller', 'پرفروش'))

    class Meta:
        verbose_name = 'کتاب'
        verbose_name_plural = 'کتاب ها'
        ordering = ["label", "-create_date"]

    id = models.UUIDField(primary_key=True, db_index=True, default=uuid.uuid4, editable=False)
    label = models.CharField(choices=LABEL, max_length=12)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    create_date = models.DateTimeField(auto_now_add=True)
    price = models.FloatField(default=0.0)
    category = models.ManyToManyField(Category, related_name='books_cat')
    discount = models.FloatField(blank=True, null=True, default=0)
    picture = models.ImageField(upload_to='picture/', blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book_details', args=[str(self.id)])

    def get_add_to_cart_url(self):
        return reverse("add-to-cart", kwargs={"pk": self.pk})

    def get_remove_from_cart_url(self):
        return reverse("remove-from-cart", kwargs={"pk": self.pk})


class Inventory(models.Model):
    """for num of book in inventory"""

    class Meta:
        verbose_name = 'موجودی'
        verbose_name_plural = 'موجودی ها'
        ordering = ["count_use"]

    book = models.ForeignKey(Book, on_delete=models.DO_NOTHING, related_name='books_inv')
    count_use = models.IntegerField(default=0)
    cont_new = models.IntegerField(default=1)

    def __str__(self):
        return self.book.title + ': ' + str(self.cont_new)

    def add_inventory(self, num):
        """for update inventory"""
        self.cont_new += num
        self.save()

    def reduce_inventory(self, num):
        """for update inventory after buy"""
        if num > self.cont_new:
            self.cont_new -= num
            self.save()
        else:
            print('inventory is empty')


class DiscountCode(models.Model):
    """this is for invoice if have a code distinct"""

    class Meta:
        verbose_name = 'کد تخفیف'
        verbose_name_plural = 'کدهای تخفیف'

    code = models.CharField(max_length=50, unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    active = models.BooleanField()

    def __str__(self):
        return self.code


class Discount(models.Model):
    """this is for book"""

    class Meta:
        verbose_name = 'تخفیف'
        verbose_name_plural = 'تخفیف ها'

    DISCOUNT = (('Percent', 'درصدی'), ('Cash', 'نقدی'),)

    type_discount = models.CharField(max_length=12, choices=DISCOUNT)
    amount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], blank=True, null=True)
    percent = models.DecimalField(decimal_places=2, max_digits=5, blank=True, null=True)
    max_use = models.IntegerField('Max number of items')
    active = models.BooleanField(default=True)
    book = models.ManyToManyField(Book, related_name='book_off')

    def __str__(self):
        return self.type_discount
