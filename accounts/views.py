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

    if request.method == "POST":

        if request.POST["password1"] == request.POST["password2"]:

            form = RegisterUserForm(request.POST)

            if form.is_valid():
                form.save()  # DB 저장

                # 회원가입 하자 마자,  로그인을 시켜줌
                username = form.cleaned_data.get(
                    "username"
                )  # request.POST.get("username",'')
                raw_password = form.cleaned_data.get("password1")
                user = authenticate(
                    username=username, password=raw_password
                )  # 사용자 인증
                login(request, user)  # 로그인

            return redirect("/")
        else:
            pass

        return render(request, "register.html")
    else:
        form = RegisterUserForm()

    return render(request, "accounts/register.html", {"form": form})
