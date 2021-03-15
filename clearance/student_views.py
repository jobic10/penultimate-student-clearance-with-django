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
    count = Logbook.objects.filter(student=student).count()
    context = {
        'page_title': 'Dashboard',
        'percent_present': count,
        'pending': Logbook.objects.filter(student=student, remark=None).count()
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


def get_weeks_from_today(date):
    pass


def add_new_logbook(request):
    status = 'New'
    student = get_object_or_404(Student, admin=request.user)
    logbook_count = Logbook.objects.filter(student=student).count()
    if logbook_count == 0:  # Empty
        form = LogForm(request.POST or None)
        week = 0
    else:  # Records Exist
        student_start_date = student.start_date
        date = datetime.datetime.today().strftime('%Y-%m-%d')
        date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
        days = abs(student_start_date - date).days
        week = days // 7

        # Check if it Student has reached the MAX_WEEK
        if week > settings.NO_OF_WEEKS:
            messages.error(request, "Sorry, you have completed your SIWES")
            return redirect(reverse('student_home'))

        # Now, we check if the week difference is exactly this week
        # If it is, show the recent logbook for update...
        # If and only If it has not been commented on by the supervisor
        if logbook_count == 1:
            instance = Logbook.objects.get(student=student)
            if instance.remark is None:
                form = LogForm(request.POST or None, instance=instance)
                status = 'Update'
            else:
                messages.success(
                    request, "Your industrial-based supervisor has commented/signed on the report from this week. You can not modify this anymore.")
                return redirect(reverse('my_logbook'))
        else:
            # Check if week is not this week, if not show new form
            instance = Logbook.objects.filter(
                student=student).order_by('-week')[0]
            if week > instance.week:  # Show new form
                form = LogForm(request.POST or None)
            else:
                if instance.remark is None:
                    form = LogForm(request.POST or None, instance=instance)
                    print("**" * 10)
                else:
                    status = 'Update'
                    messages.error(
                        request, "Your industrial-based supervisor has commented/signed on the report from this week. You can not modify this anymore. Kindly take a look at the comment")
                    return redirect(reverse('view_logbook'))
    if week == 0:
        d_week = week + 1
    else:
        d_week = week
    context = {'form': form,
               'page_title': status + ' Weekly Report / (Week ' + str(d_week) + ' )'}
    if request.method == 'POST':
        if form.is_valid():
            if logbook_count < 1:  # Does not exist, first week
                week = 1
                if not datetime.datetime.today().isoweekday == 1:  # Today is not Monday, so get the last Monday
                    # Get last monday from today
                    today = datetime.datetime.today()
                    date = today + \
                        datetime.timedelta(
                            days=-today.weekday(), weeks=0)  # I have no clue how this code works. But guess what? It works
                    # Additionally, update the start_date in Student
                monday = date
                student.start_date = monday
                student.save()
            logbook = form.save(commit=False)
            logbook.student = student
            logbook.week = week
            # Figure out the Logbook Week
            logbook.save()
            messages.success(request, "Week " +
                             str(d_week) + " Successfully Added")
        else:
            messages.error(request, "Invalid Data Provided ")
    return render(request, 'admin_template/add_logbook_template.html', context)


def view_logbook(request, logbook_id):
    me = request.user
    logbook = get_object_or_404(Logbook, id=logbook_id)
    if logbook.student != me.student:
        messages.error(request, "Sorry, you do not have access to this")
        return redirect(reverse('company_students'))
    context = {
        'logbook': logbook,
        'page_title': 'View Logbook',
    }
    return render(request, "student_template/view_logbook.html", context)


def view_my_logbook(request):
    me = request.user
    logbooks = Logbook.objects.filter(student=me.student).order_by('-week')
    context = {
        'logbooks': logbooks,
        'page_title': 'View Logbook',
    }
    return render(request, "student_template/view_student_logbook.html", context)
