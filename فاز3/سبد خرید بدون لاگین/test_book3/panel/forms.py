from django import forms
from product.models import Book


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'
        # exclude = ('slug',)
        # list_display = ['name', 'slug']
        # prepopulated_fields = {'slug': ('name',)}
