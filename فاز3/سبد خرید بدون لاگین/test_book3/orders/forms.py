from django import forms
from .models import Invoice
from accounts.models import Address

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Invoice
        # fields = ['first_name', 'last_name', 'email', 'address', 'user']
        fields = ['first_name', 'last_name', 'email', 'address']

    def __init__(self, user, *args, **kwargs):
        super(OrderCreateForm, self).__init__(*args, **kwargs)
        self.fields['address'].queryset = Address.objects.filter(user=user)
