from rest_framework import serializers
from clearance.models import *


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['fullname', 'regno', 'phone', 'gender',
                  'department', 'picture', 'direct_entry', 'admin', 'cleared']
