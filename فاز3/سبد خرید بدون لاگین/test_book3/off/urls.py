from django.urls import path
from . import views
from .views import DiscountDetailView

app_name = 'off'
urlpatterns = [
    path('off_apply/', views.off_code_apply, name='off_apply'),
    path('discount/<int:pk>/', DiscountDetailView.as_view(), name='discount_detail'),
]
