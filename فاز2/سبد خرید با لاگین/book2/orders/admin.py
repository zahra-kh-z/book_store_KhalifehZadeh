from django.contrib import admin
from .models import *


# Register your models here.

# class InvoiceItemInline(admin.StackedInline):
#     model = InvoiceItem
#
#
# @admin.register(Invoice)
# class InvoiceAdmin(admin.ModelAdmin):
#     # search_fields = ["first_name", "last_name", "email"]
#     field = '__all__'
#     inlines = [InvoiceItemInline]
#     # inlines = (InvoiceItemInline,)


admin.site.register(Invoice)
admin.site.register(InvoiceItem)

