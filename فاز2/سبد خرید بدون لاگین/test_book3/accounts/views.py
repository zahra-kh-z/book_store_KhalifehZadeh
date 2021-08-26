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


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, email=cd['email'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'you logged in successfully', 'success')
                return redirect('product:product_list')
            else:
                messages.error(request, 'username or password is wrong', 'danger')
    else:
        form = UserLoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def user_logout(request):
    logout(request)
    messages.success(request, 'you logged out successfully', 'success')
    return redirect('product:product_list')


def user_register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.create_user(cd['email'], cd['full_name'], cd['password'])
            user.save()
            messages.success(request, 'you registered successfully', 'success')
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


@login_required
def delete_user(request):
    user = User.objects.get(address__addr_ord__user_id=request.user)
    # کاربر غیرفعال میشود.برای حذف کامل باید ریموو کرد
    # ادمین میتواند کاربر فعال را فعال کند.
    user.is_active = False
    user.save()
    logout(request)
    return redirect('account:delete_confirmation')


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
    address = Address.objects.filter(pk=id, user=request.user).delete()
    return redirect("accounts:addresses")


@login_required
def set_default(request, id):
    Address.objects.filter(user=request.user, default=True).update(default=False)
    Address.objects.filter(pk=id, user=request.user).update(default=True)
    return redirect("accounts:addresses")
