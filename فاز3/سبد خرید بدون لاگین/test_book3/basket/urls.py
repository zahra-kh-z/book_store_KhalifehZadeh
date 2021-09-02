from django.urls import path
from . import views

app_name = 'basket'
urlpatterns = [
    path('', views.basket_detail, name='basket_detail'),
    path('add/<int:product_id>/', views.basket_add, name='basket_add'),
    path('remove/<int:product_id>/', views.basket_remove, name='basket_remove'),
    path('check_inventory/<int:product_id>/', views.check_inventory, name='check_inventory'),
]
