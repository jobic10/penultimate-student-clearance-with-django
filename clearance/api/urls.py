from .views import *
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('student/<int:id>', student_detail, name='detail'),
    path("login", obtain_auth_token, name="login"),
    path("reset_password", reset_password, name="reset_password"),
    path("upload_docs", upload_docs, name="upload_docs"),
    path("my_docs", my_docs, name="my_docs"),
    path("upload_status/<int:upload_id>",
         get_upload_status, name="get_upload_status"),
]
