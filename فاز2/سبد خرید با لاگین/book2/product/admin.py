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
    search_fields = ["title", "author"]
    # field = '__all__'
    list_display = ['title','slug', 'label', 'price','create_date', 'available']
    list_filter = ['label', 'create_date', 'category']
    list_editable = ['price', 'available', 'label']
    prepopulated_fields = {'slug': ('title',)}

