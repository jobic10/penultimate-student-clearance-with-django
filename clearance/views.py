from django.shortcuts import render, redirect, reverse, get_object_or_404
from .email_backend import EmailBackend
from django.contrib import messages
from django.contrib.auth import login, logout
from .models import *

# Create your views here.


def login_page(request):
    if request.user.is_authenticated:
        if request.user.user_type == '1':
            return redirect(reverse("admin_home"))
        elif request.user.user_type == '2':
            return redirect(reverse("officer_home"))
        else:
            return redirect(reverse("student_home"))
    return render(request, 'portal/login.html')


def doLogin(request, **kwargs):
    if request.method != 'POST':
        return HttpResponse("<h4>Access Denied</h4>")
    else:
        # Authenticate
        user = EmailBackend.authenticate(request, username=request.POST.get(
            'email'), password=request.POST.get('password'))
        if user != None:
            login(request, user)
            if user.user_type == '1':
                return redirect(reverse("admin_home"))
            elif user.user_type == '2':
                return redirect(reverse("officer_home"))
            else:
                return redirect(reverse("student_home"))
        else:
            messages.error(request, "Invalid details")
            return redirect("/")


def logout_user(request):
    if request.user != None:
        logout(request)
    return redirect("/")


def print_report(request, student_id):
    pass
