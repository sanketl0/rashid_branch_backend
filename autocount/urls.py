"""autocount URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import include, path, re_path

# myapp/views.py
from rest_framework import generics, status
from rest_framework.response import Response

import time
from registration.views import RequestCallView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import UserDashboardView
from django.http import HttpResponse
import socket

def simple_response(request):
    hostname = socket.gethostname()
    internal_ip = socket.gethostbyname(hostname)
    print(internal_ip)
    return HttpResponse(internal_ip,status=200)
urlpatterns = [
    path('', simple_response),
    path('admin/', admin.site.urls),
    path('company/', include('company.urls')),
    path('coa/', include('coa.urls')),
    path('item/', include('item.urls')), 
    path('salescustomer/', include('salescustomer.urls')),
    path('purchase/', include('purchase.urls')),
    path('accounting/', include('accounting.urls')),
    path('banking/', include('banking.urls')),
    path('report/', include('report.urls')),
    # path('login/', include('login.urls')),
    path('report/', include('report.urls')),
    path('transaction/', include('transaction.urls')), 
    path('registration/', include('registration.urls')),
    path('payment/', include('payment.urls')),
    path('statement/', include('statement.urls')),
    path('ocr/', include('ocr.urls')),
    path('integration/', include('integration.urls')),
    path('registration/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('request-call/',RequestCallView.as_view()),
    path('subuser/',include('subuser.urls')),
    path('userList/',UserDashboardView.as_view()),

 
]
