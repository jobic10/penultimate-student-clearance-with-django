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


    path("department/add", admin_views.add_department, name='add_department'),
    path("department/manage/", admin_views.manage_department,
         name='manage_department'),

    path("department/edit/<int:department_id>",
         admin_views.edit_department, name='edit_department'),

    path("document/add", admin_views.add_document, name='add_document'),
    path("document/manage/", admin_views.manage_document,
         name='manage_documents'),

    path("document/edit/<int:document_id>",
         admin_views.edit_document, name='edit_document'),


    path("officer/delete/<int:officer_id>",
         admin_views.delete_officer, name='delete_officer'),






    # * Officer
    path("officer/home/", officer_views.officer_home, name='officer_home'),
    path("officer_view_profile", officer_views.officer_view_profile,
         name='officer_view_profile'),
    path("officer/students/", officer_views.view_students,
         name='officer_students'),



    # * Student
    path("student/home/", student_views.student_home, name='student_home'),
    path("student_view_profile", student_views.student_view_profile,
         name='student_view_profile'),


]
