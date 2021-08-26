from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid


# Create your models here.
class DiscountCode(models.Model):
    """this is for invoice if have a code distinct, the code is unique and it for one order"""

    code = models.CharField(max_length=50, unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    active = models.BooleanField()

    class Meta:
        verbose_name = 'کد تخفیف'
        verbose_name_plural = 'کدهای تخفیف'

    def __str__(self):
        return self.code


class Category(models.Model):
    """type category for books"""

    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product:product_list_by_category', args=[self.slug])
        # return reverse('product:product_list_by_category', args=[self.id])


class Book(models.Model):
    """for register feature of book"""
    LABEL = (('New', 'جدید'), ('BestSeller', 'پرفروش'))

    class Meta:
        verbose_name = 'کتاب'
        verbose_name_plural = 'کتاب ها'
        ordering = ["label", "-create_date"]
        index_together = (('id', 'slug'),)

    """
    بعد از تکمیل کد، اتریبیوت uuid جایگزین شود
    """
    # id = models.UUIDField(primary_key=True, db_index=True, default=uuid.uuid4, editable=False)
    label = models.CharField(choices=LABEL, max_length=12)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    create_date = models.DateTimeField(auto_now_add=True)
    price = models.FloatField(default=0.0)
    # price = models.BigIntegerField(default=0.0)
    category = models.ManyToManyField(Category, related_name='books_cat')
    # category = models.ForeignKey(Category, related_name='books_cat', on_delete=models.CASCADE)
    # discount = models.FloatField(blank=True, null=True, default=0)
    picture = models.ImageField(upload_to='picture/', blank=True, null=True)
    slug = models.SlugField(max_length=200, db_index=True)
    available = models.BooleanField(default=True)

    # discount = models.ManyToManyField(Discount, related_name='book_off', blank=True, null=True, default=0)
    inventory = models.IntegerField(default=0)
    can_backorder = models.BooleanField(default=False)

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
            return f"Cannot purchase. inventory is {self.inventory}"
        return "Purchase"

    def has_inventory(self):
        if self.inventory > 0:
            a = self.inventory
        return self.inventory > 0  # True or False
        # return self.i/nventory  # True or False

    def remove_items_from_inventory(self, count=1, save=True):
        current_inv = self.inventory
        current_inv -= count
        self.inventory = current_inv
        if save == True:
            self.save()
        return self.inventory

    def __str__(self):
        return self.title

    # def get_absolute_url(self):
    #     return reverse('shop:book_details', args=[str(self.id)])

    def get_absolute_url(self):
        return reverse('product:product_list', args=[self.id, self.slug])
        # return reverse("product:product_list", kwargs={'id':self.id,'slug': self.slug})
        # return reverse('product:product_list', args=[self.id])
        # return reverse('product:product_list', args=[str(self.id), self.slug])

    def get_add_to_cart_url(self):
        # return reverse("product:add-to-cart", kwargs={"pk": self.pk})
        return reverse("product:add-to-cart", kwargs={"slug": self.slug})

    def get_remove_from_cart_url(self):
        # return reverse("product:remove-from-cart", kwargs={"pk": self.pk})
        return reverse("ecommerce:remove-from-cart", kwargs={'slug': self.slug})

    def get_absolute_url2(self):
        return reverse('product:product_detail',
                       args=[self.id, self.slug])



"""
برای محصولات شگفت انگیز و پرفروش از این مدل استفاده کن
ارتباط با محصول را چک کن (یه جایی ارور داشت ولی خودش رفع شد)
"""
class Inventory(models.Model):
    """for num of book in inventory"""

    book = models.ForeignKey(Book, on_delete=models.DO_NOTHING, related_name='books_inv')
    count_use = models.IntegerField(default=0)
    cont_new = models.IntegerField(default=1)

    class Meta:
        verbose_name = 'موجودی'
        verbose_name_plural = 'موجودی ها'
        ordering = ["count_use"]

    def has_inventory(self):
        return self.cont_new > 0  # True or False

    @property
    def can_order(self):
        if self.has_inventory():
            return True
        return False

    def __str__(self):
        return self.book.title + ': ' + str(self.cont_new)

    def check_inventory(self, quantity):
        # item = self.book['title']
        # quantity = self.book['quantity']
        # if (quantity > item.cont_new):
        #     raise ValidationError("Insufficient inventory")

        if quantity > self.cont_new:
            # go to set address
            self.reduce_inventory(quantity)
        else:
            print('inventory is empty')

        # def clean(self):
        #     product_id = self.product_id
        #     product = Product.objects.get(id=self.product_id)
        #     quantity = self.cleaned_data['quantity']
        #     if product.stock < quantity:
        #         raise forms.ValidationError(
        #             f"The maximum stock available is {product.stock}")

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


class Discount(models.Model):
    """this is for book"""

    DISCOUNT = (('Percent', 'درصدی'), ('Cash', 'نقدی'),)

    type_discount = models.CharField(max_length=12, choices=DISCOUNT)
    amount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], blank=True, null=True)
    percent = models.DecimalField(decimal_places=2, max_digits=5, blank=True, null=True)
    max_use = models.IntegerField('Max number of items')
    active = models.BooleanField(default=True)

    book = models.ManyToManyField(Book, related_name='book_off')

    class Meta:
        verbose_name = 'تخفیف'
        verbose_name_plural = 'تخفیف ها'

    def __str__(self):
        return self.type_discount
