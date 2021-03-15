from django.shortcuts import render, HttpResponse, get_object_or_404, redirect, reverse
from django.views.decorators.csrf import csrf_exempt
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.core.mail import send_mail
import requests as r
from django.template.loader import render_to_string
from django.conf import settings
# Create your views here.


def admin_home(request):
    total_officer = Officer.objects.all().count()
    total_student = Student.objects.all().count()
    total_department = Department.objects.all().count()
    context = {
        'page_title': "Administrative Dashboard",
        'total_students': total_student,
        'total_officers': total_officer,
        'total_departments': total_department,

    }
    return render(request, 'admin_template/home_content.html', context)


@csrf_exempt
def check_email_availability(request):
    email = request.POST.get("email")
    try:
        user = CustomUser.objects.filter(email=email).exists()
        if user:
            return HttpResponse(True)
        return HttpResponse(False)
    except Exception as e:
        return HttpResponse(False)


def add_student(request):
    form = StudentForm(request.POST or None, request.FILES or None)
    admin = CustomUserForm(request.POST or None)
    context = {'form': form, 'page_title': 'Add Student'}
    if request.method == 'POST':
        if form.is_valid() and admin.is_valid():
            student = form.save(commit=False)
            admin = admin.save(commit=False)
            admin.user_type = 3  # 3 Stands for Student

            # Send mail
            data = {'msg': "Welcome, Please use this password to login your account <b>" +
                    str(request.POST.get('password'))+"</b> ", 'SITENAME': settings.APP_NAME}
            msg_html = render_to_string(
                'email/email.html', data)
            msg_plain = render_to_string(
                'email/email.txt', data)
            admin.save()
            student.admin = admin
            student.save()
            messages.success(request, "Successfully Added")
            context['form'] = StudentForm()
            try:
                send_mail(
                    'Account Creation',
                    msg_plain,
                    settings.EMAIL_HOST_USER,
                    [request.POST.get('email')],
                    html_message=msg_html,
                )
            except:
                pass
        else:
            messages.error(request, "Invalid Data Provided ")
    return render(request, 'admin_template/add_student_template.html', context)


def admin_view_profile(request):
    admin = get_object_or_404(Admin, admin=request.user)
    form = CustomUserForm(
        request.POST or None, request.FILES or None, instance=admin.admin)
    context = {'form': form,
               'page_title': 'View/Edit Profile'
               }
    print(str(admin.admin.__dict__))
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
    return render(request, "admin_template/admin_view_profile.html", context)


def manage_student(request):
    students = CustomUser.objects.filter(user_type=3)
    context = {
        'students': students,
        'page_title': 'Manage Students'
    }
    return render(request, "admin_template/manage_student.html", context)


def edit_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    form = StudentEditForm(request.POST or None,
                           request.FILES or None, instance=student)
    form2 = CustomUserForm(request.POST or None, instance=student.admin)
    context = {
        'form': form,
        'form2': form2,
        'student_id': student_id,
        'page_title': 'Edit Student'
    }
    if request.method == 'POST':
        if form.is_valid() and form2.is_valid():
            form.save()
            form2.save()
            messages.success(request, "Successfully Updated")
            return redirect(reverse('edit_student', args=[student_id]))
        else:
            messages.error(request, "Please Fill Form Properly!")
    else:
        return render(request, "admin_template/edit_student_template.html", context)


def admin_view_profile(request):
    print(request.user)
    admin = get_object_or_404(Admin, admin=request.user)
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
    return render(request, "admin_template/admin_view_profile.html", context)


def manage_officer(request):
    officers = CustomUser.objects.filter(user_type=2)
    context = {
        'officers': officers,
        'page_title': 'Manage Officers'
    }
    return render(request, "admin_template/manage_officer.html", context)


def manage_department(request):
    depts = Department.objects.all()
    context = {
        'departments': depts,
        'page_title': 'Manage Departments'
    }
    return render(request, "admin_template/manage_department.html", context)


def manage_logbook(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id', 0)
        student = get_object_or_404(Student, id=student_id)
        remark = request.POST.get('remark', None)
        if remark is None:
            messages.error(request, "Please fill in the remark!")
        else:
            obj, created = FinalRemark.objects.update_or_create(
                student=student, defaults={'remark': remark})
            messages.success(request, "Action Saved")
    students = CustomUser.objects.filter(user_type=3)
    context = {
        'students': students,
        'page_title': 'View Student\'s Logbook'
    }
    return render(request, "admin_template/manage_logbook.html", context)


def add_department(request):
    form = DepartmentForm(request.POST or None)
    context = {'form': form, 'page_title': 'Add Department'}
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            context['form'] = DepartmentForm()
            messages.success(request, "Department Created")
        else:
            messages.error(request, "Invalid Form")
    return render(request, 'admin_template/add_department_template.html', context)


def edit_department(request, department_id):
    department = get_object_or_404(Department, id=department_id)
    form = DepartmentForm(request.POST or None, instance=department)
    context = {
        'form': form,
        'department_id': department_id,
        'page_title': 'Edit Department'
    }
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully Updated")
            return redirect(reverse('edit_department', args=[department_id]))
        else:
            messages.error(request, "Please Fill Form Properly!")
    else:
        return render(request, "admin_template/edit_department_template.html", context)


def add_officer(request):
    form = OfficerForm(request.POST or None, request.FILES or None)
    admin = CustomUserForm(request.POST or None)
    context = {'form': form, 'form2': admin, 'page_title': 'Add Officer'}
    if request.method == 'POST':
        if form.is_valid() and admin.is_valid():
            officer = form.save(commit=False)
            admin = admin.save(commit=False)
            admin.user_type = 2  # 2 Stands for Officer
            admin.save()
            officer.admin = admin
            officer.save()
            messages.success(request, "Successfully Added")
            context['form'] = OfficerForm()
            context['form2'] = CustomUserForm()
        else:
            messages.error(request, "Invalid Data Provided ")
    return render(request, 'admin_template/add_officer_template.html', context)


def edit_officer(request, officer_id):
    officer = get_object_or_404(Officer, id=officer_id)
    form = OfficerForm(request.POST or None,
                       request.FILES or None, instance=officer)
    form2 = CustomUserForm(request.POST or None, instance=officer.admin)
    context = {
        'form': form,
        'form2': form2,
        'officer_id': officer_id,
        'page_title': 'Edit Officer'
    }
    if request.method == 'POST':
        if form.is_valid() and form2.is_valid():
            form.save()
            form2.save()
            messages.success(request, "Successfully Updated")
            return redirect(reverse('edit_officer', args=[officer_id]))
        else:
            messages.error(request, "Please Fill Form Properly!")
    else:
        return render(request, "admin_template/edit_officer_template.html", context)


def delete_officer(request, officer_id):
    officers = CustomUser.objects.filter(user_type=2)
    context = {
        'officers': officers,
        'page_title': 'Manage Officers'
    }
    officer = get_object_or_404(Officer, id=officer_id)
    admin = officer.admin
    # Check if any student is assigned to this officer
    exist = Student.objects.filter(officer=officer).count()
    if exist > 0:
        messages.error(request, "Sorry, there exists " + str(exist) +
                       " students assigned to this Officer. What would you like to do about this ?")
    else:
        admin.delete()
        officer.delete()  # Delete Officer and Delete User

        messages.success(request, "Officer has been deleted.")

    return redirect(reverse('manage_officer'))
