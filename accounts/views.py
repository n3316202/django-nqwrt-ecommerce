from django.shortcuts import render
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

from .forms import RegisterUserForm


# dev_9
# Create your views here.
def logout_user(request):
    logout(request)
    return redirect("/")


# dev_9
def login_user(request):

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "You Have been logged in")
            return redirect("/")
        else:
            messages.success(request, ("There was an error, please try again"))
            return redirect("login")
    else:
        return render(request, "accounts/login.html", {})


def register_user(request):
    form = RegisterUserForm()

    if request.method == "POST":

        if request.POST["password1"] == request.POST["password2"]:
            user = User.objects.create_user(
                username=request.POST["username"],
                password=request.POST["password1"],
                email=request.POST["email"],
            )
            login(request, user)
            return redirect("/")
        else:
            pass

        return render(request, "register.html")
    else:
        context = {"form": form}

    return render(request, "accounts/register.html", context)
