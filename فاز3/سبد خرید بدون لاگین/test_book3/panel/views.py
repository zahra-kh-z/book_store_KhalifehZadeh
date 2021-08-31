from django.shortcuts import render
from django.views.generic.base import View
from django.views.generic.base import TemplateView
from accounts.models import *

from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy
from product.models import *
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin  # new
from django.core.exceptions import PermissionDenied  # new
from off.models import *
from persiantools.jdatetime import JalaliDateTime


# Create your views here.
class admin(TemplateView):
    model = User
    template_name = 'panel/admin.html'


class staff(TemplateView):
    model = User
    template_name = 'panel/staff.html'


class customer(TemplateView):
    model = User
    template_name = 'panel/customer.html'


# books
class BookListView(LoginRequiredMixin, ListView):  # new
    model = Book
    template_name = 'panel/book_list.html'
    login_url = 'login'  # new


class BookTableListView(LoginRequiredMixin, ListView):  # new
    model = Book
    template_name = 'panel/datatable.html'
    login_url = 'login'  # new


class BookDetailView(LoginRequiredMixin, DetailView):  # new
    model = Book
    template_name = 'panel/book_detail.html'
    login_url = 'login'  # new


class BookCreateView(UserPassesTestMixin, CreateView):  # new
    model = Book
    template_name = 'panel/book_new.html'
    # fields = ('name', 'price', 'author',)
    fields = '__all__'
    login_url = 'login'  # new

    def form_valid(self, form):  # new
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.is_staffs


class BookUpdateView(UserPassesTestMixin, UpdateView):  # new
    model = Book
    # fields = ('title', 'body',)
    fields = '__all__'
    template_name = 'panel/book_edit.html'
    login_url = 'login'  # new

    def dispatch(self, request, *args, **kwargs):  # new
        obj = self.get_object()
        if obj.user != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def test_func(self):
        return self.request.user.is_staffs


class BookDeleteView(UserPassesTestMixin, DeleteView):  # new
    model = Book
    template_name = 'panel/book_delete.html'
    success_url = reverse_lazy('panel:book_list')
    login_url = 'login'  # new

    def dispatch(self, request, *args, **kwargs):  # new
        obj = self.get_object()
        if obj.user != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def test_func(self):
        return self.request.user.is_staffs


# category
class CategoryListView(LoginRequiredMixin, ListView):  # new
    model = Category
    template_name = 'panel/category_list.html'
    login_url = 'login'  # new


class CategoryDetailView(LoginRequiredMixin, DetailView):  # new
    model = Category
    template_name = 'panel/category_detail.html'
    login_url = 'login'  # new


class CategoryCreateView(UserPassesTestMixin, CreateView):  # new
    model = Category
    template_name = 'panel/category_new.html'
    # fields = ('name', 'price', 'author',)
    fields = '__all__'
    login_url = 'login'  # new

    def form_valid(self, form):  # new
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.is_staffs


class CategoryUpdateView(UserPassesTestMixin, UpdateView):  # new
    model = Category
    # fields = ('title', 'body',)
    fields = '__all__'
    template_name = 'panel/category_edit.html'
    login_url = 'login'  # new

    def dispatch(self, request, *args, **kwargs):  # new
        obj = self.get_object()
        if obj.user != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def test_func(self):
        return self.request.user.is_staffs


class CategoryDeleteView(UserPassesTestMixin, DeleteView):  # new
    model = Category
    template_name = 'panel/category_delete.html'
    success_url = reverse_lazy('panel:category_list')
    login_url = 'login'  # new

    def dispatch(self, request, *args, **kwargs):  # new
        obj = self.get_object()
        if obj.user != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def test_func(self):
        return self.request.user.is_staffs


# discount
class DiscountListView(LoginRequiredMixin, ListView):  # new
    model = Discount
    template_name = 'panel/discount_list.html'
    login_url = 'login'  # new


class DiscountDetailView(LoginRequiredMixin, DetailView):  # new
    model = Discount
    template_name = 'panel/discount_detail.html'
    login_url = 'login'  # new


class DiscountCreateView(UserPassesTestMixin, CreateView):  # new
    model = Discount
    template_name = 'panel/discount_new.html'
    # fields = ('name', 'price', 'author',)
    fields = '__all__'
    login_url = 'login'  # new

    def form_valid(self, form):  # new
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.is_staffs


class DiscountUpdateView(UserPassesTestMixin, UpdateView):  # new
    model = Discount
    # fields = ('title', 'body',)
    fields = '__all__'
    template_name = 'panel/discount_edit.html'
    login_url = 'login'  # new

    def dispatch(self, request, *args, **kwargs):  # new
        obj = self.get_object()
        if obj.user != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def test_func(self):
        return self.request.user.is_staffs


class DiscountDeleteView(UserPassesTestMixin, DeleteView):  # new
    model = Discount
    template_name = 'panel/discount_delete.html'
    success_url = reverse_lazy('panel:discount_list')
    login_url = 'login'  # new

    def test_func(self):
        return self.request.user.is_staffs

    # def dispatch(self, request, *args, **kwargs):  # new
    #     obj = self.get_object()
    #     if obj.user != self.request.user:
    #         raise PermissionDenied
    #     return super().dispatch(request, *args, **kwargs)


# discount code
class DiscountCodeListView(LoginRequiredMixin, ListView):  # new
    model = DiscountCode
    template_name = 'panel/discountcode/discountcode_list.html'
    login_url = 'login'  # new


class DiscountCodeDetailView(LoginRequiredMixin, DetailView):  # new
    model = DiscountCode
    template_name = 'panel/discountcode/discountcode_detail.html'
    login_url = 'login'  # new


class DiscountCodeCreateView(UserPassesTestMixin, CreateView):  # new
    model = DiscountCode
    template_name = 'panel/discountcode/discountcode_new.html'
    # fields = ('name', 'price', 'author',)
    fields = '__all__'
    login_url = 'login'  # new

    def form_valid(self, form):  # new
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.is_staffs


class DiscountCodeUpdateView(UserPassesTestMixin, UpdateView):  # new
    model = DiscountCode
    # fields = ('title', 'body',)
    fields = '__all__'
    template_name = 'panel/discountcode/discountcode_edit.html'
    login_url = 'login'  # new

    def dispatch(self, request, *args, **kwargs):  # new
        obj = self.get_object()
        if obj.user != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def test_func(self):
        return self.request.user.is_staffs


class DiscountCodeDeleteView(UserPassesTestMixin, DeleteView):  # new
    model = DiscountCode
    template_name = 'panel/discountcode/discountcode_delete.html'
    success_url = reverse_lazy('panel:discountcode_list')
    login_url = 'login'  # new

    def test_func(self):
        return self.request.user.is_staffs


def my_time(request):
    # my_t = JalaliDateTime.now().to_gregorian()
    my_t = JalaliDateTime.now()
    return render(request, 'panel/admin.html', {'my_t': my_t})


def book_by_off(request):
    books = Discount.objects.all()
    # book_count =Discount.objects.all().count()
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
