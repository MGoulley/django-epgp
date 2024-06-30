# -*- encoding: utf-8 -*-
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import *

def login_view(request):
    form = LoginForm(request.POST or None)

    msg = 'Se connecter'

    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("indexadmin")
            else:
                msg = 'Mot de passe invalide'
        else:
            msg = 'Impossible de se connecter'

    return render(request, "accounts/login.html", {"form": form, "msg" : msg})
