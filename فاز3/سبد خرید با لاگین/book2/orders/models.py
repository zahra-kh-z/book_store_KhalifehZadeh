from django.conf import settings
from django.db import models
from decimal import Decimal
from product.models import Book, Discount, DiscountCode
from myusers.models import Customer, Address


# Create your models here.


class InvoiceItem(models.Model):
    class Meta:
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارش ها'

    # invoice = models.ForeignKey(Invoice, on_delete=models.PROTECT, related_name='items')
    # book = models.ForeignKey(Book, on_delete=models.DO_NOTHING, related_name='order_items')
    item = models.ForeignKey(Book, on_delete=models.CASCADE)
    price = models.IntegerField(null=True, blank=True)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.item.title + ': ' + str(self.quantity)

    def off_book2(self):
        return self.item.off_b()


    def price_book_after_off(self):
        """calculate price of book if have a discount"""
        if self.item.book_off.amount:
            """calculate price with discount ,if 1 book of 100 with 50 would be 100-50 = 50 """
            price_off = self.price - self.item.book_off.amount

        elif self.item.book_off.percent:
            """calculate price with discount ,if 1 book of 100 with 25% would be 100*0.25 = 75 """
            price_off = self.price * self.item.book_off.percent
        else:
            price_off = self.price
        return price_off

    def price_off(self):
        # for test
        # b = self.item.discount.get(book_off__discount__type_discount='Cash')
        b = self.item.book_off.get(book__book_off__type_discount='Cash')
        if b.amount:
            price_off = (self.item.price * self.quantity)- b.amount
        else:
            price_off = self.price
        return price_off
        # return a.count(),b.amount

    @property
    def get_cost(self):
        """calculate price by quantity with discount ,if 4 book of 100 with 25% would be 400*0.25 = 300 """
        return self.price_book_after_off() * self.quantity

    def get_difference_price_after_discount(self):
        """if 4 book of 100 with 25% would be (400 - 400*0.25 = 100) """
        return (self.quantity * self.item.price) - self.get_cost()

    def get_price(self):
        """if 4 book of 100 with 25% would be (400 - 400*0.25 = 100) """
        return self.quantity * self.item.price


class Invoice(models.Model):
    class Meta:
        ordering = ["created"]  # ordering by the created field
        verbose_name = 'سبد خرید'
        verbose_name_plural = 'سبدهای خرید'

    STATUS_CHOICES = (('Pending', 'سفارش'), ('Delivered', 'ثبت شده'))
    # customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING, related_name='customer_ord')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default='Pending')
    created = models.DateTimeField(auto_now_add=True)
    discount = models.ForeignKey(DiscountCode, related_name='discounts_ord', null=True, blank=True,
                                 on_delete=models.CASCADE)
    total_price = models.BigIntegerField(null=True, blank=True)
    ordered = models.BooleanField(default=False)

    items = models.ManyToManyField(InvoiceItem)

    email = models.EmailField(unique=True, blank=True, null=True)
    address = models.ForeignKey(Address, on_delete=models.DO_NOTHING, related_name='addr_ord', blank=True, null=True)

    # def __str__(self):
    #     return self.customer.full_name() + " " + self.status

    def __str__(self):
        return f'{self.user}_{self.status}'

    def check_sabt(self):
        """for check inventory before register and  then decrease inventory"""
        order_items = InvoiceItem.objects.filter(invoice_id=self.id)
        for ord_item in order_items:
            if ord_item.quantity > ord_item.item.inventory:
                print('inventory is empty')
            break
        else:
            for ord_item in order_items:
                ord_item.item.inventory -= ord_item.quantity

    def placeOrder(self):
        self.save()

    # def get_total_price(self):
    #     """for calculate total price of invoice and count price if have a code of distinct"""
    #     total = sum(item.get_cost() for item in self.items.all())
    #     if self.discount:
    #         discount_price = (self.discount.discount / Decimal('100')) * total
    #         return int(total - discount_price)
    #     return total

    def get_total_price(self):
        """for calculate total price of invoice and count price if have a code of distinct"""
        # total = sum(item.get_price() for item in self.items.all())
        total = sum(item.price_off() for item in self.items.all())
        return total

    def get_items(self):
        return self.items.all()

    # @staticmethod
    # def get_orders_by_customer(customer_id):
    #     return Invoice.objects.filter(customer=customer_id).order_by('-created')
