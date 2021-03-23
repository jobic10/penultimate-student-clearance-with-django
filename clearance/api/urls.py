from .views import *
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('student/<int:id>', student_detail, name='detail'),
    path("login", obtain_auth_token, name="login"),
    path("reset_password", reset_password, name="reset_password"),
]
