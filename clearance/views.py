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
        return HttpResponse("<h4>Denied</h4>")
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
    # user = request.user
    # student = get_object_or_404(Student, id=student_id)
    # logbooks = Logbook.objects.filter(student=student)
    # try:
    #     if user.user_type == '1':  # Admin
    #         pass
    #     elif user.user_type == '2':  # Officer
    #         if user.company != student.company:
    #             messages.error(request, "Sorry, access to this is denied")
    #             return redirect(reverse('company_home'))
    #     elif user.user_type == '3':  # Student
    #         if user.student != student:
    #             messages.error(request, "You do not have access to this!")
    #             return redirect(reverse('student_home'))
    #     else:
    #         messages.error(request, "You are unknown")
    #         return redirect(reverse('student_home'))
    # except:
    #     messages.error(request, "Something about you is not right!")
    #     return redirect(reverse('student_home'))

    # context = {'logbooks': logbooks,
    #            'page_title': "Logbook", 'student': student}
    # return render(request, "portal/logbook_report.html", context)
