from django.contrib import admin

# Register your models here.
from .models import Category, Book, Inventory

admin.site.register(Inventory)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Book)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'discount_book', 'available', 'created', 'updated', 'label']
    search_fields = ['name', "author"]
    # field = '__all__'
    list_filter = ['available', 'created', 'updated', 'label']
    # list_editable = ['_price', 'available', 'label']
    list_editable = ['price', 'available', 'label']
    prepopulated_fields = {'slug': ('name',)}
