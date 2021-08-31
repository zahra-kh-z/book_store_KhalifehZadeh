from django.contrib import admin
from .models import *


# Register your models here.
class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    raw_id_fields = ['product']


@admin.register(Invoice)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'status', 'first_name', 'last_name', 'email', 'address', 'paid', 'created', 'updated',]
    list_filter = ['status', 'created', 'updated']
    inlines = [InvoiceItemInline]
    list_editable = ['status', 'email', 'address', 'paid']
    search_fields = ['email']

    def status(self, obj):
        return obj.status
