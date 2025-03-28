from django.shortcuts import render
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


# dev_8
# Create your views here.
def logout_user(request):
    logout(request)
    return redirect("/")
