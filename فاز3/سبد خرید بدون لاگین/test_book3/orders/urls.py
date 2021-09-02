from django.urls import path
from . import views
from .apiviews import *
from orders.views import *

app_name = 'orders'
urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path('user_orders/', views.user_orders, name='user_orders'),
    path('all_orders/', views.all_orders, name='all_orders'),

    # for download report orders
    path("orders_excel_list/", OrdersList.as_view(), name="orders_excel_list"),
    path("all_orders_json/", AllOrdersList.as_view(), name="all_orders_json"),

]
