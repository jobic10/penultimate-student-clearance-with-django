from django.urls import path
from . import officer_views, admin_views, student_views, views

urlpatterns = [
    # * General
    path("", views.login_page, name='login_page'),
    path("doLogin/", views.doLogin, name='user_login'),
    path("logout_user/", views.logout_user, name='user_logout'),
    path("report/student/<int:student_id>/print/",
         views.print_report, name="generate_report"),

    # * Admin
    path("admin/home/", admin_views.admin_home, name='admin_home'),
    path("admin/student/add", admin_views.add_student, name="add_student"),
    path("check_email_availability", admin_views.check_email_availability,
         name="check_email_availability"),
    path("admin_view_profile", admin_views.admin_view_profile,
         name='admin_view_profile'),
    path("student/manage/", admin_views.manage_student, name='manage_student'),
    path("student/edit/<int:student_id>",
         admin_views.edit_student, name='edit_student'),
    path("officer/add", admin_views.add_officer, name='add_officer'),
    path("officer/manage/", admin_views.manage_officer, name='manage_officer'),

    path("officer/edit/<int:officer_id>",
         admin_views.edit_officer, name='edit_officer'),

    path("officer/delete/<int:officer_id>",
         admin_views.delete_officer, name='delete_officer'),
    path('logbook/view/all', admin_views.manage_logbook, name='manage_logbook'),






    # * Officer
    path("officer/home/", officer_views.officer_home, name='officer_home'),
    path("officer_view_profile", officer_views.officer_view_profile,
         name='officer_view_profile'),
    path("officer/logbook/<int:logbook_id>", officer_views.view_logbook,
         name='officer_view_logbook'),
    path("officer/student/<int:student_id>/logbook", officer_views.view_student_logbook,
         name='student_logbook'),
    path("officer/students/", officer_views.view_students,
         name='officer_students'),
    path("officer/logbook/<int:logbook_id>/update/",
         officer_views.update_logbook, name='update_logbook'),
    path('officer/mass/remark', officer_views.mass_remark, name='mass_remark'),




    # * Student
    path("student/home/", student_views.student_home, name='student_home'),
    path("student_view_profile", student_views.student_view_profile,
         name='student_view_profile'),


]
