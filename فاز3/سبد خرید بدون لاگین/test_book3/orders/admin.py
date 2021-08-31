from django.contrib import admin
from .models import *
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


class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    raw_id_fields = ['product']


@admin.register(Invoice)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'status', 'first_name', 'last_name', 'email', 'address', 'paid', 'created', 'updated', ]
    list_filter = ['status', 'created', 'updated']
    inlines = [InvoiceItemInline]
    list_editable = ['status', 'email', 'address', 'paid']
    search_fields = ['email']
    actions = ["export_as_csv"]

    def status(self, obj):
        return obj.status
