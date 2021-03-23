from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from clearance.models import *
from .serializers import *


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def student_detail(request, id):
    try:
        student = Student.objects.get(id=id)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    user = request.user
    if user.student != student:
        return Response({'response': "You do not have access to this resource", 'error': True})
    serializer = StudentSerializer(student)
    return Response(serializer.data)


@api_view(['PUT', ])
@permission_classes((IsAuthenticated,))
def change_password(request, id):
    try:
        student = Student.objects.get(id=id)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = ChangePasswordSerializer(data=request.data)
    if serializer.is_valid():
        old_password = serializer.data.get("old_password")
        user = request.user
        user.check_password(old_password)
    serializer = StudentSerializer(student, data=request.data)
    data = {}
    if serializer.is_valid():
        serializer.save()
        data["status"] = "Success"
        return Response(data=data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE', ])
def delete_upload(request, id):
    pass
