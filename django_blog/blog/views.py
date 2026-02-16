from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import RegisterForm, ProfileForm


# LOGIN
def user_login(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('profile')

        else:
            messages.error(request, "Invalid username or password")


    return render(request, "blog/login.html")


# LOGOUT
def user_logout(request):
    logout(request)
    return redirect('login')


# REGISTER
def register(request):

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully")
            return redirect('login')

    else:
        form = RegisterForm()

    return render(
        request,
        "blog/register.html",
        {"form": form}
    )


# PROFILE
@login_required
def profile(request):

    if request.method == "POST":

        form = ProfileForm(
            request.POST,
            instance=request.user
        )

        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated")

    else:
        form = ProfileForm(instance=request.user)


    return render(
        request,
        "blog/profile.html",
        {"form": form}
    )
