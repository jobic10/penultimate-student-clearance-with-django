from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from clearance.models import *
from .serializers import *


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def student_detail(request):
    user = request.user
    serializer = StudentSerializer(user.student)
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
    my_docs = list(Document.objects.values_list('pk').exclude(category=cat))
    if document not in my_docs:
        data["error"] = True
        data['msg'] = "You do not have access to this resource"
        return Response(data, status=status.HTTP_400_BAD_REQUEST)
    # ! Check if the incoming upload is an existing upload that needs to be modified
    # ! If exists, check status and if status is approved, do not save the form
    doc = Document.objects.get(id=doc)
    student = Upload(student=user.student,
                     document=doc)
    previous_document = Upload.objects.filter(
        student=user.student, document=doc)
    if previous_document.exists():
        # ! Check status, if approved
        if previous_document[0].approved:
            data["error"] = True
            data["msg"] = "This document has already been approved. You are not allowed to re-upload!"
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        serializer = UploadDocumentSerializer(
            previous_document[0], data=request.data)
    else:
        serializer = UploadDocumentSerializer(student, data=request.data)
    if serializer.is_valid():
        try:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except:
            data["error"] = True
            data["msg"] = "You have already uploaded this document "
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
    else:
        data['error'] = True
        data['msg'] = serializer.errors
        print(serializer.errors)

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


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_upload_status(request, upload_id):
    user = request.user
    upload = Upload.objects.filter(id=upload_id)
    data = {}
    if upload.exists():
        upload = upload[0]
        if upload.student != user.student:
            data["error"] = True
            data["msg"] = "You do not have access to this resource "
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        if upload.approved:
            msg = "Approved"
        else:
            if upload.remark is None:
                msg = "Pending"
            else:
                msg = "Not Approved : " + str(upload.remark)
        data['error'] = False
        data['msg'] = msg
        return Response(data)
    else:
        data['error'] = True
        data['msg'] = "Access Denied"
        return Response(data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def my_uploads(request):
    user = request.user
    data = {}
    uploads = Upload.objects.filter(student=user.student).order_by('-approved')
    if uploads.exists():
        data['error'] = False
        data['msg'] = "There are " + str(len(uploads)) + " uploads"
        uploads = UploadSerializer(uploads, many=True)
        data['uploads'] = uploads.data
    else:
        data['error'] = True
        data['msg'] = 'You are yet to make any uploads!'
    print(data)
    return Response(data)
