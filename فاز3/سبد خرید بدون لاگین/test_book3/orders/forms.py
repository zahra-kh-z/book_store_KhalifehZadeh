from django import forms
from .models import Invoice
from accounts.models import Address


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Invoice
        # fields = ['first_name', 'last_name', 'email', 'address', 'user']  # show user address and save in admin
        fields = ['first_name', 'last_name', 'email', 'address', 'status']

    def __init__(self, user, *args, **kwargs):
        super(OrderCreateForm, self).__init__(*args, **kwargs)
        # if default=True the address cant be delete, id del order can delete addr, show all address user
        # self.fields['address'].queryset = Address.objects.filter(user=user)
        # only show default address for orders
        self.fields['address'].queryset = Address.objects.filter(user=user, default=True)
