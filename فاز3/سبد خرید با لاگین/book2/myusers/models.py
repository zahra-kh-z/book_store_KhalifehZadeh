from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.db.models import Q

# Create your models here.
# from orders.models import Invoice


# from django.contrib.auth.models import User
# class Customer(models.Model):
#     user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
#     name = models.CharField(max_length=200, null=True, blank=True)
#     email = models.CharField(max_length=200, null=True, blank=True)


class Customer(models.Model):
    """information of customer"""

    class Meta:
        verbose_name = 'مشتری'
        verbose_name_plural = 'مشتریان'

    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=20)
    email = models.EmailField(unique=True, blank=False)
    phone = models.CharField(max_length=24, blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    code_off = models.CharField(max_length=50, unique=True, blank=True, null=True)

    def __str__(self):
        return self.first_name + '-' + self.last_name

    def full_name(self):
        return self.first_name + ' ' + self.last_name


class Address(models.Model):
    """multi address for customer. one of them is primary for register"""
    street = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=10, blank=True, null=True)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=40, blank=True, null=True)
    is_primary = models.BooleanField(null=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    # if One2Many is better than FK, each customer have multi address, but one address is for just one customer
    customer = models.ForeignKey("Customer", on_delete=models.CASCADE, related_name="addr_customer")

    # order = models.ForeignKey(Invoice, on_delete=models.SET_NULL, null=True)

    def save(self, *args, **kwargs):
        if self.is_primary:
            self.__class__._default_manager.filter(customer=self.customer, is_primary=True).update(is_primary=False)
        super().save(*args, **kwargs)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['customer'], condition=Q(is_primary=True),
                                    name='unique_primary_per_customer')]
        verbose_name = 'آدرس'
        verbose_name_plural = 'آدرس ها'

    def __str__(self):
        return self.country + '-' + self.city + '-' + self.postal_code


class User(AbstractBaseUser):
    """for admin and staff (employee)"""

    class Meta:
        verbose_name = 'کامند'
        verbose_name_plural = 'کارمندان'

    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)  # a admin user, non super-user
    admin = models.BooleanField(default=False)  # a superuser

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Email & Password are required by default.


    """
    برای فاز 3 دسترسی های کاربران را اینجا مشخص کن. با پرمیشن یا مدل گروپ
    (توضیحات خانم قانعی و خانم متین فر در مورد یوزرهای جنگو چک شود- جلسه حل تمرین)
     ساخت یک مدل جدید و ارث بری یوزرها سرچ شود
    """

    def get_full_name(self):
        """user is identified by their email address"""
        return self.email

    def get_short_name(self):
        """user is identified by their email address"""
        return self.email

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        """Is the user a member of staff?"""
        return self.staff

    @property
    def is_admin(self):
        """Is the user a admin member?"""
        return self.admin
