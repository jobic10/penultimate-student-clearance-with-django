from .views import *
from django.urls import path


urlpatterns = [
    path('<int:id>', student_detail, name='detail'),
]
