from django.contrib.auth.decorators import login_required
from accounts.forms import UserEditForm
from orders.views import user_orders
from .forms import UserLoginForm, UserRegistrationForm
from django.contrib.auth import authenticate, login, logout
from .models import User
from .models import Address
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import UserAddressForm
from django.contrib.auth import login
from django.views.generic import CreateView
from .forms import StaffSignUpForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from orders.views import Invoice
from django.db.models import Count
from persiantools.jdatetime import JalaliDateTime
from product.models import Book
from off.models import Discount
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from .forms import RegistrationForm
from .tokens import account_activation_token

"""______ all method for user ______"""


def user_login(request):
    """for login with email and password"""
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
    """for logout users"""
    logout(request)
    messages.success(request, 'خروج با موفقیت انجام شد.', 'success')
    return redirect('product:product_list')


def user_register(request):
    """
    for register all users
    without send email for activate
    """
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.create_user(cd['email'], cd['full_name'], cd['password'])
            user.save()
            messages.success(request, 'ثبت نام با موفقیت انجام شد.', 'success')
            return redirect('product:product_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def dashboard(request):
    """show all activity of users, for see this page user should be login"""
    orders = user_orders(request)
    return render(request, 'panel/ords.html', {'orders': orders})


@login_required
def edit_details(request):
    """for edit info of users, for see this page user should be login"""
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
    """
    This method is used to delete the user.
    But the user is not deleted completely. The user is inactivate.
    Only the administrator is allowed to reactivate the user.
    """
    user = User.objects.get(email=request.user.email)
    user.is_active = False
    user.save()
    logout(request)
    return redirect('accounts:delete_user')


def change_password(request):
    """for change password by user, should be login"""
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'پسورد با موفقیت آپدیت شد.')
            return redirect('accounts:login')
        else:
            messages.error(request, 'لطفا خطاهای زیر را اصلاح کنید.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {
        'form': form
    })


def all_users(request):
    """for count all users, all users by date,
     for report to admin panel.
     """
    users_count = User.objects.filter(is_staffs=False, is_admin=False).count()
    from django.db.models import Count
    users_by_date = User.objects.filter(is_staffs=False, is_admin=False).extra({'created': "date(created)"}).values(
        'created').annotate(count=Count('id'))

    return render(request, 'accounts/all_users.html',
                  {'users_count': users_count, 'users_by_date': users_by_date, })


"""______ all methode for Addresses ______"""


@login_required
def view_address(request):
    """show all user address"""
    addresses = Address.objects.filter(user=request.user)
    # for add address by modal
    if request.method == "POST":
        address_form = UserAddressForm(data=request.POST)
        if address_form.is_valid():
            address_form = address_form.save(commit=False)
            address_form.user = request.user
            address_form.save()
            return HttpResponseRedirect(reverse("accounts:addresses"))
    else:
        address_form = UserAddressForm()

    return render(request, "account/dashboard/addresses.html", {"addresses": addresses, "form": address_form})


@login_required
def add_address(request):
    """add address for user"""
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
    """for edit info of address by user"""
    if request.method == "POST":
        address = Address.objects.get(pk=id, user=request.user)
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
    """delete address by user, but one address remain"""
    address = Address.objects.filter(pk=id, user=request.user, default=False).delete()
    return redirect("accounts:addresses")


@login_required
def set_default(request, id):
    """Selects an address as the default address for sending the order. """
    Address.objects.filter(user=request.user, default=True).update(default=False)
    Address.objects.filter(pk=id, user=request.user).update(default=True)
    return redirect("accounts:addresses")


@login_required
def user_addr(request):
    """
    for show all address of a user
    but if you want default address, should filter query by default field.
    we use default address in form for orders.
    """
    addr = Address.objects.filter(user=request.user)
    return render(request, "order/create.html'", {"addr": addr})


"""______ all methode for register staff ______"""


class StaffSignUpView(CreateView):
    """
    for register a staff.
    but we use below method for register staff by admin.
    """
    model = User
    form_class = StaffSignUpForm
    template_name = 'accounts/register.html'

    def get_context_data(self, **kwargs):
        kwargs['is_staff'] = True
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('panel:staff')


def register_staff(request):
    """
    In this method, only the manager can register an employee.
    """
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.create_user(cd['email'], cd['full_name'], cd['password'])
            user.is_staffs = True
            user.save()
            messages.success(request, 'ثبت نام با موفقیت انجام شد.', 'success')
            return redirect('product:product_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})


"""______ methode for panel admin reports ______"""


def reports(request):
    """
    In this method, reports related to orders, users, JalaliDateTime and book discounts are specified.
    """
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


"""
for register user by email and send activate email for users
"""


def account_activate(request, uidb64, token):
    """
    for register user by email and send activate email for users
    """
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('accounts:dashboard')
    else:
        return render(request, 'account/registration/activation_invalid.html')


def account_register(request):
    """
    for register user by email and send activate email for users
    """
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')

    if request.method == 'POST':
        registerForm = RegistrationForm(request.POST)
        if registerForm.is_valid():
            user = registerForm.save(commit=False)
            user.email = registerForm.cleaned_data['email']
            user.set_password(registerForm.cleaned_data['password'])
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate your Account'
            message = render_to_string('account/registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject=subject, message=message)
            return render(request, 'account/registration/register_email_confirm.html', {'form': registerForm})
    else:
        registerForm = RegistrationForm()
    return render(request, 'account/registration/register.html', {'form': registerForm})
