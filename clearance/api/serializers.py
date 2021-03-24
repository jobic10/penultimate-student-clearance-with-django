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


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'name', 'category']


class UploadDocumentSerializer(serializers.HyperlinkedModelSerializer):
    # # department = serializers.CharField(source='department.name')
    class Meta:
        model = Upload
        fields = ['file']


class UploadSerializer(serializers.ModelSerializer):
    document = serializers.CharField(source='document.name')

    class Meta:
        model = Upload
        fields = ['file', 'remark', 'document', 'approved']
