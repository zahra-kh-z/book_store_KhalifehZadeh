from django import forms
from orders.models import Invoice
from orders.models import *


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['address', 'email']
