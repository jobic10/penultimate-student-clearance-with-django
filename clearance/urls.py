from django.urls import path
from . import company_views, admin_views, student_views, views

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
    path("company/add", admin_views.add_company, name='add_company'),
    path("company/manage/", admin_views.manage_company, name='manage_company'),

    path("company/edit/<int:company_id>",
         admin_views.edit_company, name='edit_company'),

    path("company/delete/<int:company_id>",
         admin_views.delete_company, name='delete_company'),
    path('logbook/view/all', admin_views.manage_logbook, name='manage_logbook'),






    # * Company
    path("company/home/", company_views.company_home, name='company_home'),
    path("company_view_profile", company_views.company_view_profile,
         name='company_view_profile'),
    path("company/logbook/<int:logbook_id>", company_views.view_logbook,
         name='company_view_logbook'),
    path("company/student/<int:student_id>/logbook", company_views.view_student_logbook,
         name='student_logbook'),
    path("company/students/", company_views.view_students,
         name='company_students'),
    path("company/logbook/<int:logbook_id>/update/",
         company_views.update_logbook, name='update_logbook'),
    path('company/mass/remark', company_views.mass_remark, name='mass_remark'),




    # * Student
    path("student/home/", student_views.student_home, name='student_home'),
    path("student_view_profile", student_views.student_view_profile,
         name='student_view_profile'),
    path("logbook/new", student_views.add_new_logbook, name="add_new_logbook"),
    path("student/logbook/<int:logbook_id>", student_views.view_logbook,
         name='view_this_logbook'),
    path("student/logbook", student_views.view_my_logbook,
         name='my_logbook'),

]
