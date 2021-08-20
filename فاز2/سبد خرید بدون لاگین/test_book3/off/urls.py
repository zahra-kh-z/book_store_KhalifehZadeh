from django.urls import path
from . import views

app_name = 'off'
urlpatterns = [
    path('off_apply/', views.off_code_apply, name='off_apply'),
]
