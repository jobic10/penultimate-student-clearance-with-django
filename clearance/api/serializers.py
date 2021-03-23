from rest_framework import serializers
from clearance.models import *


class StudentSerializer(serializers.ModelSerializer):
    department = serializers.CharField(source='department.name')

    class Meta:
        model = Student
        fields = ['fullname', 'regno', 'phone', 'gender',
                  'department', 'picture', 'direct_entry', 'admin', 'cleared']


class ChangePasswordSerializer(serializers.Serializer):
    model = CustomUser

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
