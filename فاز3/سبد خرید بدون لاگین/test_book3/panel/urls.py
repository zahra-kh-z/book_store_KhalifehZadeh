from django.urls import path, include
from accounts.forms import PwdResetForm, PwdResetConfirmForm
from .views import *
from django.contrib.auth import views as auth_views
from . import views

app_name = 'panel'
urlpatterns = [
    path('admin/', admin.as_view(), name='admin'),
    path('staff/', staff.as_view(), name='staff'),
    path('customer/', customer.as_view(), name='customer'),

    # book
    path('book_list/', BookListView.as_view(), name='book_list'),
    path('table_list/', BookTableListView.as_view(), name='book_table'),
    path('<int:pk>/', BookDetailView.as_view(), name='book_detail'),  # new
    path('new/', BookCreateView.as_view(), name='book_new'),  # new
    path('<int:pk>/edit/', BookUpdateView.as_view(), name='book_edit'),  # new
    path('<int:pk>/delete/', BookDeleteView.as_view(), name='book_delete'),  # new

    # path('^', include('django.contrib.auth.urls')),

    # category
    path('category_list/', CategoryListView.as_view(), name='category_list'),
    path('cat/<int:pk>/', CategoryDetailView.as_view(), name='category_detail'),  # new
    path('cat/new/', CategoryCreateView.as_view(), name='category_new'),  # new
    path('cat/<int:pk>/edit/', CategoryUpdateView.as_view(), name='category_edit'),  # new
    path('cat/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category_delete'),  # new

    # discount
    path('discount_list/', DiscountListView.as_view(), name='discount_list'),
    path('discount/<int:pk>/', DiscountDetailView.as_view(), name='discount_detail'),  # new
    path('discount/new/', DiscountCreateView.as_view(), name='discount_new'),  # new
    path('discount/<int:pk>/edit/', DiscountUpdateView.as_view(), name='discount_edit'),  # new
    path('discount/<int:pk>/delete/', DiscountDeleteView.as_view(), name='discount_delete'),  # new

    # تاریخ شمسی
    path('time/', my_time, name='my_time'),

    path('book_by_off/', views.book_by_off, name='book_by_off'),
]
