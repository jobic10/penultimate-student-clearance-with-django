from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from clearance.models import *
from .serializers import *


@api_view(['GET', ])
def student_detail(request, id):
    try:
        student = Student.objects.get(id=id)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = StudentSerializer(student)
    return Response(serializer.data)
