"""snak URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path
from snaksite.views import index, pick_background,take_pic,save_photo,pick_pic,record_pic,print_pic
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', index, name='index'),
    path('pick_background/', pick_background, name='pick_background'),
    path('take_pic/', take_pic, name='take_pic'),
    path('pick_pic/', pick_pic, name='pick_pic'),
    path('save_photo/', save_photo, name='save_photo'),
    path('record_pic/', record_pic, name='record_pic'),
    path('print_pic/', print_pic, name='print_pic'),
    
]