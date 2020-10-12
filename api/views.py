from django.contrib.auth import authenticate
from django.http import request # to manually authenticate user
from django.views.decorators.csrf import csrf_exempt # to use POST req without csrf
from rest_framework.authtoken.models import Token # generates/ get token for authenticated user
from rest_framework.decorators import api_view, permission_classes # some usefull decorators
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly # allowing all users to interact with the view
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_202_ACCEPTED,
    HTTP_204_NO_CONTENT
) # Some Basic HTTP responses
from rest_framework.response import Response, response # sending json response

# Some required imports
import json
from .models import * 
from .serializers import *


@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def welcome(request):
    return Response("Welcome To API IGConnect API", status=HTTP_200_OK)


@csrf_exempt
@api_view(["POST", "GET", "PUT", "DELETE"])
@permission_classes((IsAuthenticatedOrReadOnly))
def event(request):
    try:
        if request.method == "POST":
            return Response({"created": "OK"}, status=HTTP_201_CREATED)
        else:
            eventId = request.GET.get("eventId", -1)
            if(eventId == -1):
                return Response({"error": True, "message": 'parameter eventId not passed'}, status=HTTP_400_BAD_REQUEST)
            if request.method == "GET":
                return Response({"data": "data"}, status=HTTP_200_OK)
            elif request.method == "PUT":
                return Response({"message": "event update success"}, status=HTTP_202_ACCEPTED)
            elif request.method == "DELETE":
                return Response({"message": "event delete success"}, status=HTTP_204_NO_CONTENT)
    except Event.DoesNotExist as err:
        return Response({"message": "event does not exists"}, status=HTTP_404_NOT_FOUND)
    except Exception as err:
        return Response({"error": True, "message": json.dump(err)})


@csrf_exempt
@api_view(["POST", "GET", "PUT", "DELETE"])
@permission_classes((IsAuthenticatedOrReadOnly))
def timeline(request, eventId):
    try:
        event = Event.objects.get(id = eventId)
        if request.method == "POST":
            return Response({"created": "OK"}, status=HTTP_201_CREATED)
        else:
            if(eventId == -1):
                return Response({"error": True, "message": 'parameter eventId not passed'}, status=HTTP_400_BAD_REQUEST)
            if request.method == "GET":
                return Response({"data": "data"}, status=HTTP_200_OK)
            elif request.method == "PUT":
                return Response({"message": "event update success"}, status=HTTP_202_ACCEPTED)
            elif request.method == "DELETE":
                return Response({"message": "event delete success"}, status=HTTP_204_NO_CONTENT)
    except Event.DoesNotExist as err:
        return Response({"message": "event does not exists"}, status=HTTP_404_NOT_FOUND)
    except Exception as err:
        return Response({"error": True, "message": json.dump(err)})


@csrf_exempt
@api_view(["POST", "GET", "PUT", "DELETE"])
@permission_classes((IsAuthenticatedOrReadOnly))
def prize(request, eventId):
    try:
        event = Event.objects.get(id = eventId)
        if request.method == "POST":
            return Response({"created": "OK"}, status=HTTP_201_CREATED)
        else:
            if(eventId == -1):
                return Response({"error": True, "message": 'parameter eventId not passed'}, status=HTTP_400_BAD_REQUEST)
            if request.method == "GET":
                return Response({"data": "data"}, status=HTTP_200_OK)
            elif request.method == "PUT":
                return Response({"message": "event update success"}, status=HTTP_202_ACCEPTED)
            elif request.method == "DELETE":
                return Response({"message": "event delete success"}, status=HTTP_204_NO_CONTENT)
    except Event.DoesNotExist as err:
        return Response({"message": "event does not exists"}, status=HTTP_404_NOT_FOUND)
    except Exception as err:
        return Response({"error": True, "message": json.dump(err)})

@csrf_exempt
@api_view(["POST", "GET", "PUT", "DELETE"])
@permission_classes((IsAuthenticatedOrReadOnly))
def registration(request, eventId):
    try:
        event = Event.objects.get(id = eventId)
        if request.method == "POST":
            return Response({"created": "OK"}, status=HTTP_201_CREATED)
        else:
            if(eventId == -1):
                return Response({"error": True, "message": 'parameter eventId not passed'}, status=HTTP_400_BAD_REQUEST)
            if request.method == "GET":
                return Response({"data": "data"}, status=HTTP_200_OK)
            elif request.method == "PUT":
                return Response({"message": "event update success"}, status=HTTP_202_ACCEPTED)
            elif request.method == "DELETE":
                return Response({"message": "event delete success"}, status=HTTP_204_NO_CONTENT)
    except Event.DoesNotExist as err:
        return Response({"message": "event does not exists"}, status=HTTP_404_NOT_FOUND)
    except Exception as err:
        return Response({"error": True, "message": json.dump(err)})

