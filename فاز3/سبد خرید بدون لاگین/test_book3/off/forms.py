from django import forms
from django.utils.translation import gettext_lazy as _
from django.forms import ModelForm, DateTimeField
from off.MinimalSplitDateTimeMultiWidget import *
from django.contrib.admin import widgets
from .models import DiscountCode


class DiscountCodeApplyForm(forms.Form):
    code = forms.CharField(label=_('کدتخفیف'))


class DateInput(forms.DateInput):
    input_type = 'date'


class CodeForm(ModelForm):
    class Meta:
        model = DiscountCode
        fields = '__all__'
        widgets = {
            'valid_from': DateInput(),
            'valid_to': DateInput(),
        }
        """
        for use with DateTime in separate fields, date and time.
        if use this should comment above widgets.
        """
        # widgets = {
        #     'valid_from': widgets.AdminSplitDateTime,
        # }
        # expire_date = DateTimeField(widget=MinimalSplitDateTimeMultiWidget())
