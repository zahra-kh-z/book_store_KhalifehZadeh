from django.urls import path
from . import views
from .apiviews import *

app_name = 'orders'
urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path('user_orders/', views.user_orders, name='user_orders'),
    path('all_orders/', views.all_orders, name='all_orders'),

    path("tasks_json/", TaskList.as_view(), name="tasks_json_list"),
]
