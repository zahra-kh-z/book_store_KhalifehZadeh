"""test_book3 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

# for urlpatterns static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# for urlpatterns MEDIA
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('basket/', include('basket.urls', namespace='basket')),
    path('off/', include('off.urls', namespace='off')),
    path('', include('product.urls', namespace='product')),
    path('orders/', include('orders.urls', namespace='orders')),

]

urlpatterns += staticfiles_urlpatterns()
# for show media files in url (Browser)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
