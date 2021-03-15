from django.shortcuts import render, HttpResponse, get_object_or_404, redirect, reverse
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
# Create your views here.


def officer_home(request):
    me = get_object_or_404(Officer, admin=request.user)
    total_students = Student.objects.filter(officer=me).count()
    pending_remarks = Logbook.objects.filter(
        student__officer=me, remark=None).count()
    approved_remarks = Logbook.objects.exclude(
        student__officer=me, remark=None).count()
    context = {
        'page_title': 'Industrial-Based (Officer) Dashboard',
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


def view_logbook(request, logbook_id):
    me = request.user
    logbook = get_object_or_404(Logbook, id=logbook_id)
    if logbook.student.officer != me.officer:
        messages.error(request, "Sorry, you do not have access to this")
        return redirect(reverse('officer_students'))
    context = {
        'logbook': logbook,
        'page_title': 'View Logbook',
    }
    return render(request, "officer_template/view_logbook.html", context)


def view_student_logbook(request, student_id):
    me = request.user
    student = get_object_or_404(Student, id=student_id, officer=me.officer)
    logbooks = Logbook.objects.filter(student=student).order_by('-week')
    context = {
        'student': student,
        'logbooks': logbooks,
        'page_title': 'View Student Logbook',
    }
    return render(request, "officer_template/view_student_logbook.html", context)


def view_students(request):
    me = request.user
    students = Student.objects.filter(officer=me.officer)
    context = {
        'students': students,
        'page_title': 'View Students',
    }
    return render(request, "officer_template/view_students.html", context)


def update_logbook(request, logbook_id):
    if request.method != 'POST':
        return redirect(reverse('officer_students'))
    logbook = get_object_or_404(Logbook, id=logbook_id)
    if logbook.student.officer != request.user.officer:
        messages.error(
            request, "Sorry, you do not have access to this resource")
        return redirect(reverse('officer_students'))

    remark = request.POST.get('remark')
    if len(remark) < 5:
        messages.error(request, "Please fill the form properly!")
        return redirect(reverse('officer_students'))
    logbook.remark = remark
    logbook.save()
    messages.success(request, "Logbook Remarks Saved")
    return redirect(reverse('officer_view_logbook', args=[logbook_id]))


def mass_remark(request):
    students = Student.objects.filter(officer=request.user.officer)
    context = {'students': students, 'page_title': 'Mass Remark'}
    if request.method == 'POST':
        remark = request.POST.get('remark')
        if len(remark) < 4:
            messages.error(request, "Please fill form properly!")
            return redirect(reverse('mass_remark'))
        print(request.POST)
        if request.POST.get('all'):
            # All Outstanding From This Officer
            Logbook.objects.filter(
                student__officer=request.user.officer, remark=None).update(remark=remark)
            print(Logbook.objects.filter(
                student__officer=request.user.officer, remark=None))
        else:
            # Loop
            students = request.POST.getlist('students')
            # Remove empty elements
            students = [x for x in students if x.strip()]
            Logbook.objects.filter(
                student__pk__in=students, remark=None).update(remark=remark)
            for student in students:
                print("I am " + str(student))

        messages.success(request, "Changes Updated!")
    return render(request, "officer_template/mass_remark.html", context)
