from .views import *
from django.urls import path


urlpatterns = [
    path('student/<int:id>', student_detail, name='detail'),
]
