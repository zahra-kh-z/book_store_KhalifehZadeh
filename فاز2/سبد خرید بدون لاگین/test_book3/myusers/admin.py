from django.contrib import admin
from .models import Customer, Address, User


# Register your models here.
class CustomerAddressInline(admin.StackedInline):
    model = Address


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    inlines = [CustomerAddressInline]
    search_fields = ["first_name", "last_name", "email"]
    field = '__all__'


admin.site.register(Address)
admin.site.register(User)
