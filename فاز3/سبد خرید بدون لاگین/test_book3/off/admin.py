from django.contrib import admin
from .models import DiscountCode, Discount


# Register your models here.
@admin.register(DiscountCode)
class DiscountCodeAdmin(admin.ModelAdmin):
    list_display = ['code', 'valid_from', 'valid_to',
                    'discount', 'active']
    list_filter = ['active', 'valid_from', 'valid_to']
    search_fields = ['code']
    list_editable = ['valid_from', 'valid_to', 'discount', 'active']


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ['type_discount', 'amount', 'percent', 'book_name', 'book_price', 'book_offs']
    list_filter = ['type_discount']
    list_editable = ['amount', 'percent']
    search_fields = ['type_discount']

    def book_name(self, obj):
        all_book = obj.book.all()
        return ','.join(str(book.name) for book in all_book)

    def book_price(self, obj):
        all_book = obj.book.all()
        return [book.price for book in all_book]

    def book_offs(self, obj):
        all_book = obj.book.all()

        price_dis = []
        for book in all_book:

            if obj.type_discount == 'Cash':
                total = book.price - int(obj.amount)
            elif obj.type_discount == 'Percent':
                total = book.price - (book.price * (obj.percent / 100))
            else:
                total = int(book.price)
            book.unit_price = book.price

            if total > 0:
                book.discount_book = total
                book.price = total
            else:
                book.discount_book = 0
                book.price = 0

            book.save()
        return book.discount_book
        # return book.price
