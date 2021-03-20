import datetime
from django.shortcuts import render, HttpResponse, get_object_or_404, redirect, reverse
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.conf import settings
# Create your views here.


def student_home(request):
    student = get_object_or_404(Student, admin=request.user)
    uploads = Upload.objects.filter(student=student).count()
    context = {
        'page_title': 'Dashboard',
        'uploads': uploads,
        'student': student,
        'pending': Upload.objects.filter(student=student, approved=False).count()
    }
    return render(request, 'student_template/home_content.html', context)


def student_view_profile(request):
    admin = get_object_or_404(Student, admin=request.user)
    form = CustomUserForm(
        request.POST or None, request.FILES or None, instance=admin.admin)
    context = {'form': form,
               'page_title': 'View/Edit Profile'
               }
    if request.method == 'POST':
        try:
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, request.user)

                # adminForm.save()
                messages.success(request, "Profile Updated!")
                return redirect(reverse('admin_view_profile'))
            else:
                messages.error(request, "Invalid Data Provided")
        except Exception as e:
            messages.error(
                request, "Error Occurred While Updating Profile " + str(e))
    return render(request, "student_template/student_view_profile.html", context)


def uploadDocument(request):
    student = get_object_or_404(Student, admin=request.user)
    form = UploadForm(request.POST or None,
                      request.FILES or None, student=student)
    context = {'form': form, 'page_title': "Upload Document"}
    return render(request, 'admin_template/add_department_template.html', context)
