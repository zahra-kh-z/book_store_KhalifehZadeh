from django.contrib import admin
from .models import *


# Register your models here.
class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    raw_id_fields = ['product']


@admin.register(Invoice)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'address', 'paid', 'created', 'updated']
    list_filter = ['paid', 'created', 'updated']
    inlines = [InvoiceItemInline]
