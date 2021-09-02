from django.urls import path
from . import views
from accounts.forms import *
from django.views.generic import TemplateView
from .views import StaffSignUpView
from django.contrib.auth import views as auth_views  # for pass reset

app_name = 'accounts'
urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.user_register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),

    path("profile/edit/", views.edit_details, name="edit_details"),
    path("profile/delete_user/", views.delete_user, name="delete_user"),
    path(
        "profile/delete_confirm/",
        TemplateView.as_view(template_name="account/dashboard/delete_confirm.html"),
        name="delete_confirmation",
    ),
    # change_password
    path('change_password/', views.change_password, name='change_password'),

    # address
    path("addresses/", views.view_address, name="addresses"),
    path("add_address/", views.add_address, name="add_address"),
    path("addresses/edit/<slug:id>/", views.edit_address, name="edit_address"),
    path("addresses/delete/<slug:id>/", views.delete_address, name="delete_address"),
    path("addresses/set_default/<slug:id>/", views.set_default, name="set_default"),

    path("user_addr/", views.user_addr, name="user_addr"),

    # Reset password
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(
            template_name="account/password_reset/password_reset_form.html",
            success_url="password_reset_email_confirm",
            email_template_name="account/password_reset/password_reset_email.html",
            form_class=PwdResetForm,
        ),
        name="pwdreset",
    ),
    path(
        "password_reset_confirm/<uidb64>/<token>",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="account/password_reset/password_reset_confirm.html",
            success_url="password_reset_complete/",
            form_class=PwdResetConfirmForm,
        ),
        name="password_reset_confirm",
    ),
    path(
        "password_reset/password_reset_email_confirm/",
        TemplateView.as_view(template_name="account/password_reset/reset_status.html"),
        name="password_reset_done",
    ),
    path(
        "password_reset_confirm/OQ/password_reset_complete/",
        TemplateView.as_view(template_name="account/password_reset/reset_status.html"),
        name="password_reset_complete",
    ),

    # for add staff in register page
    path('reg_staff1/', StaffSignUpView.as_view(), name='reg_staff1'),

    # for add staff by admin
    path('add_staff/', views.register_staff, name='add_staff'),

    # reports
    path('reports/', views.reports, name='reports'),
    path('all_users/', views.all_users, name='all_users'),

]
