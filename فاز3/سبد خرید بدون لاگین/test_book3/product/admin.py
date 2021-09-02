from django.contrib import admin
from .models import Category, Book, Inventory
import csv
from django.http import HttpResponse


# Register your models here.
class ExportCsvMixin:
    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"


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
class ProductAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ['name', 'slug', 'price', 'discount_book', 'inventory', 'available', 'created', 'updated', 'label']
    search_fields = ['name', "author"]
    # field = '__all__'
    list_filter = ['available', 'created', 'updated', 'label']
    list_editable = ['price', 'available', 'label', 'inventory']
    prepopulated_fields = {'slug': ('name',)}
    # change_form_template = 'custom_change_form.html'
    actions = ["unmark_available", "mark_available", 'charge_inventory', 'decharge_inventory', "export_as_csv"]

    def unmark_available(self, request, queryset):
        queryset.update(available=False)

    def mark_available(self, request, queryset):
        queryset.update(available=True)

    def charge_inventory(self, request, queryset):
        queryset.update(inventory=90)

    def decharge_inventory(self, request, queryset):
        queryset.update(inventory=0)

# https://stackoverflow.com/questions/53616273/how-to-add-custom-action-button-in-django-admin-form-and-post-the-information
# https://books.agiliq.com/projects/django-admin-cookbook/en/latest/action_buttons.html
# class ProductAdmin(admin.ModelAdmin):
#     change_form_template = 'custom_change_form.html'
