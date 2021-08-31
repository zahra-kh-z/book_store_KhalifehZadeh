from django.contrib import admin

# Register your models here.
from .models import Category, Book, Inventory

# admin.site.register(Inventory)
@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ['book_name', 'count_use', 'cont_new']
    list_filter = ['cont_new']
    list_editable = ['cont_new', 'count_use']
    search_fields = ['cont_new']

    def book_name(self, obj):
        return obj.book.name


class BookInline(admin.StackedInline):
    model = Book.category.through
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [BookInline]
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']
    list_filter = ['name']
    list_editable = ['slug']


@admin.register(Book)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'discount_book', 'available', 'created', 'updated', 'label']
    search_fields = ['name', "author"]
    # field = '__all__'
    list_filter = ['available', 'created', 'updated', 'label']
    # list_editable = ['_price', 'available', 'label']
    list_editable = ['price', 'available', 'label']
    prepopulated_fields = {'slug': ('name',)}
