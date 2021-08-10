from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Category)
admin.site.register(Inventory)
admin.site.register(Discount)
admin.site.register(DiscountCode)


@admin.register(Book)
class CustomerAdmin(admin.ModelAdmin):
    search_fields = ["title", "author"]
    field = '__all__'
