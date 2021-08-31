from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import MyUserManager


class User(AbstractBaseUser):
    email = models.EmailField(max_length=100, unique=True)
    full_name = models.CharField(max_length=100)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staffs = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    objects = MyUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?Yes, always"
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?Yes, always"
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?All admins are staff"
        return self.is_admin


import uuid
from django.utils.translation import gettext_lazy as _


class Address(models.Model):
    """
    address for users and orders
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, verbose_name=_("User"), on_delete=models.CASCADE)
    full_name = models.CharField(_("Full Name"), max_length=150)
    phone = models.CharField(_("Phone Number"), max_length=50)
    postcode = models.CharField(_("Postcode"), max_length=50)
    address_line = models.CharField(_("Address Line 1"), max_length=255)
    town_city = models.CharField(_("Town/City/State"), max_length=150)
    delivery_instructions = models.CharField(_("Delivery Instructions"), max_length=255)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)
    default = models.BooleanField(_("Default"), default=False)

    class Meta:
        verbose_name = "آدرس"
        verbose_name_plural = "آدرس ها"

    def __str__(self):
        return f'{self.user}__{self.town_city}'


class Group(models.Model):
    name = models.CharField(max_length=128)
    members = models.ManyToManyField(User, related_name='groups')

    class Meta:
        verbose_name = "گروه"
        verbose_name_plural = "گروه ها"

    def __str__(self):
        return self.name


class Membership(models.Model):
    person = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    date_joined = models.DateField()
    invite_reason = models.CharField(max_length=64)

    class Meta:
        verbose_name = "عضو"
        verbose_name_plural = "اعضا"
