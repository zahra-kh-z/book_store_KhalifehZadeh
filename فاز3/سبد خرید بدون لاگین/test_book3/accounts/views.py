from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from accounts.forms import UserEditForm
from orders.views import user_orders
from .forms import UserLoginForm, UserRegistrationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import User
from .models import Address
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from .forms import UserAddressForm

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect

from orders.views import Invoice
from django.db.models import Count
from persiantools.jdatetime import JalaliDateTime
from product.models import Book
from off.models import Discount


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, email=cd['email'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'ورود با موفقیت انجام شد.', 'success')
                return redirect('product:product_list')
            else:
                messages.error(request, 'ایمیل یا پسورد اشتباه است.', 'danger')
    else:
        form = UserLoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def user_logout(request):
    logout(request)
    messages.success(request, 'خروج با موفقیت انجام شد.', 'success')
    return redirect('product:product_list')


def user_register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # user = User.objects.create_user(cd['email'], cd['full_name'], cd['password'])
            user = User.objects.create_user(cd['email'], cd['user_name'], cd['password'])
            user.save()
            messages.success(request, 'ثبت نام با موفقیت انجام شد.', 'success')
            return redirect('product:product_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})


def register_staff(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.create_user(cd['email'], cd['full_name'], cd['password'])
            # user.is_admin=True
            user.is_staffs = True
            user.save()
            messages.success(request, 'ثبت نام با موفقیت انجام شد.', 'success')
            return redirect('product:product_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def dashboard(request):
    orders = user_orders(request)
    return render(request,
                  'panel/ords.html',
                  {
                      'orders': orders})


@login_required
def edit_details(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)

        if user_form.is_valid():
            user_form.save()
    else:
        user_form = UserEditForm(instance=request.user)

    return render(request,
                  'account/dashboard/edit_details.html', {'user_form': user_form})


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'پسورد با موفقیت آپدیت شد.')
            return redirect('accounts:login')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {
        'form': form
    })


@login_required
def delete_user(request):
    # user = User.objects.get(address__addr_ord__user_id=request.user)
    user = User.objects.get(email=request.user.email)
    # کاربر غیرفعال میشود.برای حذف کامل باید ریموو کرد
    # ادمین میتواند کاربر فعال را فعال کند.
    user.is_active = False
    user.save()
    logout(request)
    return redirect('account:delete_confirmation')


def all_users(request):
    users_count = User.objects.filter(is_staffs=False, is_admin=False).count()
    from django.db.models import Count
    users_by_date = User.objects.filter(is_staffs=False, is_admin=False).extra({'created': "date(created)"}).values(
        'created').annotate(count=Count('id'))

    return render(request,
                  'accounts/all_users.html',
                  {
                      'users_count': users_count,
                      'users_by_date': users_by_date,
                  })


# Addresses
@login_required
def view_address(request):
    addresses = Address.objects.filter(user=request.user)
    return render(request, "account/dashboard/addresses.html", {"addresses": addresses})


@login_required
def add_address(request):
    if request.method == "POST":
        address_form = UserAddressForm(data=request.POST)
        if address_form.is_valid():
            address_form = address_form.save(commit=False)
            address_form.user = request.user
            address_form.save()
            return HttpResponseRedirect(reverse("accounts:addresses"))
    else:
        address_form = UserAddressForm()
    return render(request, "account/dashboard/edit_addresses.html", {"form": address_form})


@login_required
def edit_address(request, id):
    if request.method == "POST":
        address = Address.objects.get(pk=id, customer=request.user)
        address_form = UserAddressForm(instance=address, data=request.POST)
        if address_form.is_valid():
            address_form.save()
            return HttpResponseRedirect(reverse("accounts:addresses"))
    else:
        address = Address.objects.get(pk=id, user=request.user)
        address_form = UserAddressForm(instance=address)
    return render(request, "account/dashboard/edit_addresses.html", {"form": address_form})


@login_required
def delete_address(request, id):
    address = Address.objects.filter(pk=id, user=request.user, default=False).delete()
    return redirect("accounts:addresses")


@login_required
def set_default(request, id):
    Address.objects.filter(user=request.user, default=True).update(default=False)
    Address.objects.filter(pk=id, user=request.user).update(default=True)
    return redirect("accounts:addresses")


def reports(request):
    # orders
    orders = Invoice.objects.all()
    orders_count = Invoice.objects.all().count()
    mony = Invoice.objects.all()
    total = sum(product.get_total_cost() for product in mony)
    ord_by_date = Invoice.objects.extra({'created': "date(created)"}).values('created').annotate(count=Count('id'))
    # users
    users_count = User.objects.filter(is_staffs=False, is_admin=False).count()
    users_by_date = User.objects.filter(is_staffs=False, is_admin=False).extra({'created': "date(created)"}).values(
        'created').annotate(count=Count('id'))
    # time
    my_t = JalaliDateTime.now()
    # off
    books = Discount.objects.all()
    book_count_a = Book.objects.filter(book_off__amount__isnull=False).count()
    book_count_p = Book.objects.filter(book_off__percent__isnull=False).count()
    book_count_no = Book.objects.filter(book_off__amount__isnull=True, book_off__percent__isnull=True).count()

    return render(request,
                  'accounts/report.html',
                  {'orders': orders, 'orders_count': orders_count,
                   'total': total,
                   'ord_by_date': ord_by_date,
                   'users_count': users_count,
                   'users_by_date': users_by_date,
                   'my_t': my_t,
                   'books': books,
                   'book_count_a': book_count_a,
                   'book_count_p': book_count_p,
                   'book_count_no': book_count_no,
                   })
