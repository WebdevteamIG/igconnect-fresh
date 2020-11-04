from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt # to use POST req without csrf
from rest_framework.decorators import api_view, permission_classes # some usefull decorators

from rest_framework.permissions import (
    AllowAny, 
)
from rest_framework.serializers import Serializer # allowing all users to interact with the view


from rest_framework.status import (
    HTTP_302_FOUND, HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_202_ACCEPTED,
    HTTP_204_NO_CONTENT, HTTP_409_CONFLICT, 
    HTTP_500_INTERNAL_SERVER_ERROR,
) # Some Basic HTTP responses
from rest_framework.response import Response # sending json response

error = {
    "error" : True,
    "message": "internal server error",
}

from .models import *
from .serializers import *

@csrf_exempt
@api_view(["POST", "GET", "PUT", "DELETE",])
@permission_classes((AllowAny, ))
def submission(request):
    try:
        if(request.method == "POST"):
            serialized = SubmissionSerializer(data=request.data)
            if serialized.is_valid():
                serialized.save()
                return Response({"message": "create success"}, status=HTTP_201_CREATED)
            
            return Response({"error": True, "message": serialized.errors}, status=HTTP_400_BAD_REQUEST)

        user = request.query_params.get('email', '')
        if user == '':
            return Response({"error": True, "message": "pass a valid email id"})
        
        submission = OICSubmissions.objects.get(user=user)
        if request.method == "GET":
            serialized = SubmissionSerializer(submission)
            return Response(serialized.data, status=HTTP_200_OK)

        elif request.method == "PUT":
            serialized = SubmissionSerializer(submission, data=request.data, partial=True)
            if serialized.is_valid():
                serialized.save()
                return Response({"message": "update success"}, status=HTTP_202_ACCEPTED)
            
            return Response({"error": True, "message": serialized.errors}, status=HTTP_400_BAD_REQUEST)

        elif request.method == "DELETE":
            submission.delete()
            return Response({"message": "delete success"}, status=HTTP_204_NO_CONTENT)

    except OICSubmissions.DoesNotExist:
        return Response({"error": True, "message": "no submission exists for the requested email"}, status=HTTP_404_NOT_FOUND)

    except Exception as err:
        print(err)
        return Response(error, status=HTTP_500_INTERNAL_SERVER_ERROR)