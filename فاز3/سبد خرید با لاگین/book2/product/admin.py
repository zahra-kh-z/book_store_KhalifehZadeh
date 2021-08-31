from django.contrib import admin
from .models import *

# Register your models here.
# admin.site.register(Category)
admin.site.register(Inventory)
admin.site.register(Discount)
admin.site.register(DiscountCode)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Book)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'discount_book', 'inventory', 'available', 'created', 'updated', 'label']
    search_fields = ['name', "author"]
    list_filter = ['available', 'created', 'updated', 'label']
    list_editable = ['price', 'available', 'label', 'inventory']
    prepopulated_fields = {'slug': ('name',)}
