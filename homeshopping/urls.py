"""homeshopping URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', eviews.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path
from homeshopping import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    path('accounts/', include('accounts.urls'), name='accounts'),
    path('accounts/', include('django.contrib.auth.urls'), name='accounts'),
    path('products/', include("products.urls"), name='products'),
    path('home/', views.Homepage.as_view(), name='home'),
    path('checkout/', views.Checkout.as_view(), name='checkout'),
    path('search/', views.Search.as_view(), name='search'),
    path('', views.Homepage.as_view()),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
