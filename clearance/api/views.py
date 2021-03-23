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


@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def reset_password(request):
    # try:
    #     student = Student.objects.get(id=id)
    # except:
    #     return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = ChangePasswordSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        old_password = serializer.data.get("old_password")
        new_password = serializer.data.get("new_password")
        user = request.user
        if user.check_password(old_password):
            request.user.set_password(serializer.data.get('new_password'))
            request.user.save()
            data["error"] = False
            data["msg"] = "Password changed"
        else:
            data["error"] = True
            data["msg"] = "Old Password Not Correct"
    # # serializer = StudentSerializer(student, data=request.data)
    # if serializer.is_valid():
    #     serializer.save()
    #     data["status"] = "Success"
    #     return Response(data=data)
    return Response(data)


@api_view(['DELETE', ])
def delete_upload(request, id):
    pass
