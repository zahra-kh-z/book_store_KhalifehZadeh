from django.urls import path
from . import views
from .views import SearchResultsListView, OrderSummaryView, add_to_cart, remove_from_cart, remove_single_item_from_cart, \
    BookDetails, my_orders_view

"""
ویوهای مربوط به هر مدل در اپ خودش نوشته شود.
پوشه تمپلت جدا برای هر اپ.
برای هر اپ url در اپ مربوطه نوشته شود.
ویو مربوط به ثبت خرید، مثل پروژه session نوشته شود

"""
app_name = 'product'
urlpatterns = [
    # if move to button of path, its not work
    path('create/', views.order_create, name='order_create'),
    path('search/', SearchResultsListView.as_view(), name='search_results'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    # path('add-to-cart/<pk>/', add_to_cart2, name='add-to-cart'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('', views.product_list, name='product_list'),
    path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove-item-from-cart/<slug>/', remove_single_item_from_cart,
         name='remove-single-item-from-cart'),

    path('<int:id>/<slug:slug>/', BookDetails.as_view(), name='product_detail'),
    # path('cart/', views.cart, name="cart"),

    # path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    # path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),

    path('success/', my_orders_view, name='my_orders_view'),
    # path('checkout/', CheckoutView.as_view(), name='checkout'),


]

# path('', HomeView.as_view(), name='home'),
# with iduu answered
# path('product/<pk>/', ProductView.as_view(), name='product'),
