from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http import HttpRequest as r
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
    return Response(data)


@api_view(['DELETE', ])
def delete_upload(request, id):
    pass


@api_view(['POST', 'GET'])
@permission_classes((IsAuthenticated,))
def upload_docs(request):
    r = request
    data = {}
    user = request.user
    doc = request.POST.get('document_id', None)
    if doc is None:
        data["error"] = True
        data["msg"] = "Please choose a document"
        return Response(data, status=status.HTTP_400_BAD_REQUEST)
    document = None
    if user.student.direct_entry:
        cat = 1
    else:
        cat = 2
    try:
        document = Document.objects.values_list('id').get(id=doc)
    except:
        data["error"] = True
        data["msg"] = "Invalid Document "
        return Response(data, status=status.HTTP_400_BAD_REQUEST)
    print(document)
    my_docs = list(Document.objects.values_list('pk').exclude(category=cat))
    print(str(my_docs) + "For Id " + str(tuple(doc)))
    if document not in my_docs:
        data["error"] = True
        data['msg'] = "You do not have access to this resource"
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

    student = Upload(student=user.student,
                     document=Document.objects.get(id=doc))
    serializer = UploadDocumentSerializer(student, data=request.data)
    if serializer.is_valid():
        try:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except:
            data["error"] = True
            data["msg"] = "You have already uploaded this document "
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def my_docs(request):
    user = request.user
    if user.student.direct_entry:
        cat = 1
    else:
        cat = 2
    docs = Document.objects.exclude(category=cat)
    data = DocumentSerializer(docs, many=True)
    return Response(data.data)
