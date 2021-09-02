from django.views.generic.base import TemplateView
from accounts.models import *
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy
from product.models import *
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from off.models import *
from off.forms import CodeForm
from persiantools.jdatetime import JalaliDateTime
from .forms import BookForm

# Create your views here.
"""
Renders a given template, with the context containing parameters captured in the URL.
# https://docs.djangoproject.com/en/3.2/ref/class-based-views/base/#django.views.View
"""


class admin(TemplateView):
    template_name = 'panel/admin.html'


class staff(TemplateView):
    model = User
    template_name = 'panel/staff.html'


class customer(TemplateView):
    model = User
    template_name = 'panel/customer.html'


""" ____ all methode for Book ____"""


class BookListView(LoginRequiredMixin, ListView):
    """show list of all book for staff and admin"""
    model = Book
    template_name = 'panel/book_list.html'
    login_url = 'login'


class BookTableListView(LoginRequiredMixin, ListView):
    """show all book in a table  for staff and admin"""
    model = Book
    template_name = 'panel/datatable.html'
    login_url = 'login'  # new


class BookDetailView(LoginRequiredMixin, DetailView):
    """show details book for staff and admin"""
    model = Book
    template_name = 'panel/book_detail.html'
    login_url = 'login'


"""
for allow permission for create Book can use staff_member_required or
can use UserPassesTestMixin for allow, test is a user is staff, can create book, category , discount
"""


# https://stackoverflow.com/questions/22250352/programmatically-create-a-django-group-with-permissions
# https://stackoverflow.com/questions/65812073/only-staff-user-should-post-a-product-in-django
# https://docs.djangoproject.com/en/3.1/ref/contrib/admin/#the-staff-member-required-decorator
# from django.contrib.admin.views.decorators import staff_member_required
# @staff_member_required


class BookCreateView(UserPassesTestMixin, CreateView):
    """for create book by staff"""
    model = Book
    template_name = 'panel/book_new.html'
    fields = '__all__'
    # form_class = BookForm
    login_url = 'login'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.is_staffs


class BookUpdateView(UserPassesTestMixin, UpdateView):
    """
    for update info of book
    only a staff or admin create this, can update the book
    """
    model = Book
    fields = '__all__'
    template_name = 'panel/book_edit.html'
    login_url = 'login'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def test_func(self):
        return self.request.user.is_staffs


class BookDeleteView(UserPassesTestMixin, DeleteView):
    """
      for delete info of book
      only a staff or admin create this, can delete the book
    """
    model = Book
    template_name = 'panel/book_delete.html'
    success_url = reverse_lazy('panel:book_list')
    login_url = 'login'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def test_func(self):
        return self.request.user.is_staffs


""" ____ all methode for Category ____"""


class CategoryListView(LoginRequiredMixin, ListView):
    """show list of all category for staff and admin"""
    model = Category
    template_name = 'panel/category_list.html'
    login_url = 'login'


class CategoryDetailView(LoginRequiredMixin, DetailView):
    """show details category for staff and admin"""
    model = Category
    template_name = 'panel/category_detail.html'
    login_url = 'login'


class CategoryCreateView(UserPassesTestMixin, CreateView):
    """for create category by staff"""
    model = Category
    template_name = 'panel/category_new.html'
    fields = '__all__'
    login_url = 'login'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.is_staffs


class CategoryUpdateView(UserPassesTestMixin, UpdateView):
    """
     for update info of category
     only a staff or admin create this, can update the category
     """
    model = Category
    fields = '__all__'
    template_name = 'panel/category_edit.html'
    login_url = 'login'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def test_func(self):
        return self.request.user.is_staffs


class CategoryDeleteView(UserPassesTestMixin, DeleteView):
    """
       for delete info of category
       only a staff or admin create this, can delete the category
    """
    model = Category
    template_name = 'panel/category_delete.html'
    success_url = reverse_lazy('panel:category_list')
    login_url = 'login'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def test_func(self):
        return self.request.user.is_staffs


""" ____ all methode for discount ____"""


class DiscountListView(LoginRequiredMixin, ListView):
    """show list of all discount for staff and admin"""
    model = Discount
    template_name = 'panel/discount_list.html'
    login_url = 'login'


class DiscountDetailView(LoginRequiredMixin, DetailView):
    """show details discount for staff and admin"""
    model = Discount
    template_name = 'panel/discount_detail.html'
    login_url = 'login'


class DiscountCreateView(UserPassesTestMixin, CreateView):
    """for create discount by staff and admin"""
    model = Discount
    template_name = 'panel/discount_new.html'
    fields = '__all__'
    login_url = 'login'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.is_staffs


class DiscountUpdateView(UserPassesTestMixin, UpdateView):
    """
         for update info of discount
         only a staff or admin create this, can update the discount
     """
    model = Discount
    fields = '__all__'
    template_name = 'panel/discount_edit.html'
    login_url = 'login'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def test_func(self):
        return self.request.user.is_staffs


class DiscountDeleteView(UserPassesTestMixin, DeleteView):
    """
       for delete info of discount
       only a staff or admin create this, can delete the discount
    """
    model = Discount
    template_name = 'panel/discount_delete.html'
    success_url = reverse_lazy('panel:discount_list')
    login_url = 'login'

    def test_func(self):
        return self.request.user.is_staffs

    # def dispatch(self, request, *args, **kwargs):
    #     obj = self.get_object()
    #     if obj.user != self.request.user:
    #         raise PermissionDenied
    #     return super().dispatch(request, *args, **kwargs)


""" ____ all methode for discount code____"""


class DiscountCodeListView(LoginRequiredMixin, ListView):
    """show list of all discount code for staff and admin"""
    model = DiscountCode
    template_name = 'panel/discountcode/discountcode_list.html'
    login_url = 'login'


class DiscountCodeDetailView(LoginRequiredMixin, DetailView):
    """show details discount code for staff and admin"""
    model = DiscountCode
    template_name = 'panel/discountcode/discountcode_detail.html'
    login_url = 'login'


class DiscountCodeCreateView(UserPassesTestMixin, CreateView):
    """for create discount code by staff and admin"""
    model = DiscountCode
    template_name = 'panel/discountcode/discountcode_new.html'
    # fields = '__all__'  # if not use forms.py
    login_url = 'login'
    form_class = CodeForm
    success_url = reverse_lazy('panel:discountcode_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.is_staffs


class DiscountCodeUpdateView(UserPassesTestMixin, UpdateView):
    """
         for update info of discount code
         only a staff or admin create this, can update the discount code
     """
    model = DiscountCode
    fields = '__all__'
    template_name = 'panel/discountcode/discountcode_edit.html'
    login_url = 'login'
    success_url = reverse_lazy('panel:discountcode_list')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def test_func(self):
        return self.request.user.is_staffs


class DiscountCodeDeleteView(UserPassesTestMixin, DeleteView):
    """
       for update info of discount code
       only a staff or admin create this, can update the discount code
   """
    model = DiscountCode
    template_name = 'panel/discountcode/discountcode_delete.html'
    success_url = reverse_lazy('panel:discountcode_list')
    login_url = 'login'

    def test_func(self):
        return self.request.user.is_staffs


def my_time(request):
    """
    for show time jalali in admin panel
    https://pypi.org/project/persiantools/
    """
    # my_t = JalaliDateTime.now().to_gregorian()
    my_t = JalaliDateTime.now()
    return render(request,
                  'panel/admin.html',
                  {'my_t': my_t})


def book_by_off(request):
    """
    for show all book by discount
    and show all book without discount
    """
    books = Discount.objects.all()
    book_count_a = Book.objects.filter(book_off__amount__isnull=False).count()
    book_count_p = Book.objects.filter(book_off__percent__isnull=False).count()
    book_count_no = Book.objects.filter(book_off__amount__isnull=True, book_off__percent__isnull=True).count()
    return render(request,
                  'panel/discount_list.html',
                  {
                      'books': books,
                      'book_count_a': book_count_a,
                      'book_count_p': book_count_p,
                      'book_count_no': book_count_no,
                  })
