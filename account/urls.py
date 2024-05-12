# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from . import views
from .views import *
from django.contrib.auth.views import LogoutView

urlpatterns = [
    # Matches any html file
    re_path(r'^.*\.html', views.pages, name='pages'),

    # The home page
    path('', views.index, name='home'),

    # login
    path('accounts/login/', login_view, name="login"),
    path('accounts/register/', register_user, name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
]