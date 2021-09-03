from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import User
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from .models import Address


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'full_name')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] and cd['password2'] and cd['password1'] != cd['password2']:
            raise forms.ValidationError('passwords must match')
        return cd['password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'full_name')

    def clean_password(self):
        return self.initial['password']


class UserLoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'id': 'login-email', 'placeholder': 'email', }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class UserRegistrationForm(forms.ModelForm):
    """
    for register user without send email activate
    """
    full_name = forms.CharField(
        label='Enter Username', min_length=4, max_length=50, help_text='Required')
    email = forms.EmailField(max_length=100, help_text='Required', error_messages={
        'required': 'Sorry, you will need an email'})
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('full_name', 'email',)

    def clean_username(self):
        full_name = self.cleaned_data['full_name'].lower()
        r = User.objects.filter(full_name=full_name)
        if r.count():
            raise forms.ValidationError("Username already exists")
        return full_name

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords do not match.')
        return cd['password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'Please use another Email, that is already taken')
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['full_name'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'full_name'})
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'E-mail', 'name': 'email', 'id': 'id_email'})
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Repeat Password'})


class UserAddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ["full_name", "phone", "address_line", "town_city", "postcode"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["full_name"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "Full Name"}
        )
        self.fields["phone"].widget.attrs.update({"class": "form-control mb-2 account-form", "placeholder": "Phone"})
        self.fields["address_line"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "Full Name"}
        )

        self.fields["town_city"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "Full Name"}
        )
        self.fields["postcode"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "Full Name"}
        )

        self.fields['full_name'].label = "نام کامل"
        self.fields['phone'].label = "شماره تلفن"
        self.fields['address_line'].label = "آدرس"
        self.fields['town_city'].label = "شهر"
        self.fields['postcode'].label = "کدپستی"


class PwdResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label='New password', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'New Password', 'id': 'form-newpass'}))
    new_password2 = forms.CharField(
        label='Repeat password', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'New Password', 'id': 'form-new-pass2'}))


class PwdResetForm(PasswordResetForm):
    email = forms.EmailField(max_length=254, widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'Email', 'id': 'form-email'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        u = User.objects.filter(email=email)
        if not u:
            raise forms.ValidationError(
                'Unfortunatley we can not find that email address')
        return email


class UserEditForm(forms.ModelForm):
    email = forms.EmailField(
        label='بهتر است ایمیل خود را تغییر ندهید', max_length=200, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'email', 'id': 'form-email', }))

    full_name = forms.CharField(label='full_name', widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('email', 'full_name',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['full_name'].required = True


"""
test forms for create custom staff
"""


class StaffSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff
        if commit:
            user.save()
        return user


class StaffCreationForm(forms.ModelForm):
    """
    A Custom form for creating new staffs.
    """

    class Meta:
        model = User
        fields = ['full_name', 'email']






"""
for register users by active email
"""

class RegistrationForm(forms.ModelForm):

    full_name = forms.CharField(
        label='Enter full_name', min_length=4, max_length=50, help_text='Required')
    email = forms.EmailField(max_length=100, help_text='Required', error_messages={
        'required': 'Sorry, you will need an email'})
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('full_name', 'email',)

    def clean_username(self):
        full_name = self.cleaned_data['full_name'].lower()
        r = User.objects.filter(full_name=full_name)
        if r.count():
            raise forms.ValidationError("Username already exists")
        return full_name

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords do not match.')
        return cd['password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'Please use another Email, that is already taken')
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['full_name'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'full_name'})
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'E-mail', 'name': 'email', 'id': 'id_email'})
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Repeat Password'})