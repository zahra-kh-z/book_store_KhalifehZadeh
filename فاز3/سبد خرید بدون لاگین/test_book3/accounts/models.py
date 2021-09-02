from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import MyUserManager
from django.contrib.admin.views.decorators import staff_member_required
import uuid
from django.utils.translation import gettext_lazy as _


class User(AbstractBaseUser):
    """all users by this class create and then by permissions can work"""
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

    @property
    def is_staff(self):
        """Is the user a member of staff? All admins are staff"""
        return self.is_admin

    @staff_member_required
    def a_staff_view(self):
        """all staff allow to change view by staff_member_required"""
        return self.is_staffs

    def get_full_name(self):
        """The user is identified by their email address"""
        return self.email

    def get_short_name(self):
        """The user is identified by their email address"""
        return self.email

    def __unicode__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?Yes, always"""
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`? Yes, always"""
        return True


class Address(models.Model):
    """
    Address for all user
    multi address for customer. one of them is primary for register
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


"""
Users and permissions can also be defined as follows:
with proxy we can make 3 level of users: admin, staff, customer.
and in MyUserManager should be defined a method for create users.
then by Group can set permission for any users.
also, Instead of these models, you can use the default model of Django itself.
in this project we use User(AbstractBaseUser) for create users, and work by permissions.

"""


class Customer(User):
    """With this class, a customer user can be defined."""

    class Meta:
        proxy = True
        verbose_name = 'مشتری'
        verbose_name_plural = 'مشتریان'

    is_staffs = False
    is_admin = False


class Staffs(User):
    """With this class, a staff (employee) user can be defined."""

    class Meta:
        proxy = True
        verbose_name = 'کارمند'
        verbose_name_plural = 'کارمندان'

    is_staffs = True
    is_admin = False


class Admin(User):
    """With this class, admin user can be defined."""

    class Meta:
        proxy = True
        verbose_name = 'مدیر'
        verbose_name_plural = 'مدیران'

    is_staffs = True
    is_admin = True


class Group(models.Model):
    """
    With this model, different groups can be defined.
    Each user can then be given access to existing permissions.
    """
    name = models.CharField(max_length=128)
    members = models.ManyToManyField(User, related_name='groups')

    class Meta:
        verbose_name = "گروه"
        verbose_name_plural = "گروه ها"

    def __str__(self):
        return self.name


class Membership(models.Model):
    """
    This model specifies users and groups. Members of a group are displayed with this.
    """
    person = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    date_joined = models.DateField()
    invite_reason = models.CharField(max_length=64)

    class Meta:
        verbose_name = "عضو"
        verbose_name_plural = "اعضا"
