from django.urls import path, include
from . import views
from .views import *
# from django.contrib.auth import views as auth_views

app_name = 'panel'
urlpatterns = [
    path('admin/', admin.as_view(), name='admin'),
    path('staff/', staff.as_view(), name='staff'),
    path('customer/', customer.as_view(), name='customer'),

    # book
    path('book_list/', BookListView.as_view(), name='book_list'),
    path('table_list/', BookTableListView.as_view(), name='book_table'),
    path('<int:pk>/', BookDetailView.as_view(), name='book_detail'),
    path('new/', BookCreateView.as_view(), name='book_new'),
    path('<int:pk>/edit/', BookUpdateView.as_view(), name='book_edit'),
    path('<int:pk>/delete/', BookDeleteView.as_view(), name='book_delete'),

    # path('^', include('django.contrib.auth.urls')),

    # category
    path('category_list/', CategoryListView.as_view(), name='category_list'),
    path('cat/<int:pk>/', CategoryDetailView.as_view(), name='category_detail'),
    path('cat/new/', CategoryCreateView.as_view(), name='category_new'),
    path('cat/<int:pk>/edit/', CategoryUpdateView.as_view(), name='category_edit'),
    path('cat/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category_delete'),

    # discount
    path('discount_list/', DiscountListView.as_view(), name='discount_list'),
    path('discount/<int:pk>/', DiscountDetailView.as_view(), name='discount_detail'),
    path('discount/new/', DiscountCreateView.as_view(), name='discount_new'),
    path('discount/<int:pk>/edit/', DiscountUpdateView.as_view(), name='discount_edit'),
    path('discount/<int:pk>/delete/', DiscountDeleteView.as_view(), name='discount_delete'),

    # discount code
    path('discountcode_list/', DiscountCodeListView.as_view(), name='discountcode_list'),
    path('discountcode/<int:pk>/', DiscountCodeDetailView.as_view(), name='discountcode_detail'),
    path('discountcode/newcode/', DiscountCodeCreateView.as_view(), name='discountcode_new'),
    path('discountcode/<int:pk>/editcode/', DiscountCodeUpdateView.as_view(), name='discountcode_edit'),
    path('discountcode/<int:pk>/deletecode/', DiscountCodeDeleteView.as_view(), name='discountcode_delete'),

    path('time/', my_time, name='my_time'),
    path('book_by_off/', views.book_by_off, name='book_by_off'),
]
