from django.shortcuts import render, HttpResponse, get_object_or_404, redirect, reverse
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
# Create your views here.


def officer_home(request):
    me = get_object_or_404(Officer, admin=request.user)
    total_students = Student.objects.filter(
        department=me.department).count()
    pending_remarks = Student.objects.filter(
        department=me.department, cleared=False).count()
    approved_remarks = Student.objects.filter(
        department=me.department, cleared=True).count()
    context = {
        'page_title': 'Clearance Officer Dashboard',
        'total_students': total_students,
        'approved_remarks': approved_remarks,
        'pending_remarks': pending_remarks
    }
    return render(request, 'officer_template/home_content.html', context)


def officer_view_profile(request):
    admin = get_object_or_404(Officer, admin=request.user)
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
                return redirect(reverse('officer_view_profile'))
            else:
                messages.error(request, "Invalid Data Provided")
        except Exception as e:
            messages.error(
                request, "Error Occurred While Updating Profile " + str(e))
    return render(request, "officer_template/officer_view_profile.html", context)


def view_upload_by_id(request, id):
    me = get_object_or_404(Officer, admin=request.user)
    student = get_object_or_404(Student, id=id)
    uploads = Upload.objects.filter(student=student)
    context = {
        'uploads': uploads,
        'student': student,
        'page_title': "View Student's Uploads",
    }
    return render(request, "officer_template/view_uploads.html", context)


def view_students(request):
    me = get_object_or_404(Officer, admin=request.user)
    # students = Student.objects.filter(officer=me.officer)
    students = Student.objects.filter(
        department=me.department)
    context = {
        'students': students,
        'page_title': 'View All Students',
    }
    return render(request, "officer_template/view_students.html", context)


def pending_students(request):
    me = get_object_or_404(Officer, admin=request.user)
    # students = Student.objects.filter(officer=me.officer)
    students = Student.objects.filter(
        department=me.department, cleared=False)
    context = {
        'students': students,
        'page_title': 'View Pending Students',
    }
    return render(request, "officer_template/view_students.html", context)


def approved_students(request):
    me = get_object_or_404(Officer, admin=request.user)
    # students = Student.objects.filter(officer=me.officer)
    students = Student.objects.filter(
        department=me.department, cleared=True)
    context = {
        'students': students,
        'page_title': 'View Approved Students',
        'disable': True
    }
    return render(request, "officer_template/view_students.html", context)
