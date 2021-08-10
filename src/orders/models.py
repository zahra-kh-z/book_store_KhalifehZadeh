from django.db import models
from decimal import Decimal
from myusers.models import Customer
from product.models import Book, Discount, DiscountCode


# Create your models here.
class Invoice(models.Model):
    class Meta:
        ordering = ["created"]  # ordering by the created field
        verbose_name = 'سبد خرید'
        verbose_name_plural = 'سبدهای خرید'

    STATUS_CHOICES = (('Pending', 'سفارش'), ('Delivered', 'ثبت شده'))
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING, related_name='customer_ord')
    status = models.CharField(max_length=12, choices=STATUS_CHOICES)
    created = models.DateTimeField(auto_now_add=True)
    discount = models.ForeignKey(DiscountCode, related_name='discounts_ord', null=True, blank=True,
                                 on_delete=models.CASCADE)
    total_price = models.BigIntegerField(null=True, blank=True)

    def __str__(self):
        return self.customer.full_name() + " " + self.status

    def get_total_price(self):
        """for calculate total price of invoice and count price if have a code of distinct"""
        total = sum(item.get_cost() for item in self.items.all())
        if self.discount:
            discount_price = (self.discount.discount / Decimal('100')) * total
            return int(total - discount_price)
        return total


class InvoiceItem(models.Model):
    class Meta:
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارش ها'

    invoice = models.ForeignKey(Invoice, on_delete=models.PROTECT, related_name='items')
    book = models.ForeignKey(Book, on_delete=models.DO_NOTHING, related_name='order_items')
    price = models.IntegerField(null=True, blank=True)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.book.title + ': ' + str(self.quantity)

    def price_book_after_off(self):
        """calculate price of book if have a discount"""
        if self.book.book_off.amount:
            """calculate price with discount ,if 1 book of 100$ with 50 would be 100-50 = 50$ """
            price_off = self.price - self.book.book_off.amount

        elif self.book.book_off.percent:
            """calculate price with discount ,if 1 book of 100$ with 25% would be 100*0.25 = 75$ """
            price_off = self.price * self.book.book_off.percent
        else:
            price_off = self.price
        return price_off

    @property
    def get_cost(self):
        """calculate price by quantity with discount ,if 4 book of 100$ with 25% would be 400*0.25 = 300$ """
        return self.price_book_after_off() * self.quantity

    def get_difference_price_after_discount(self):
        """if 4 book of 100$ with 25% would be (400$ - 400*0.25 = 100$) """
        return (self.quantity * self.book.price) - self.get_cost()
