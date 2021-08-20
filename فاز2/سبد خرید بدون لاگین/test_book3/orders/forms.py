from django import forms
from .models import Invoice


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['first_name', 'last_name', 'email', 'address']
