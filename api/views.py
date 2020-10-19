from os import stat
from django.contrib.auth import authenticate
from django.db import connections
from django.http import request # to manually authenticate user
from django.views.decorators.csrf import csrf_exempt # to use POST req without csrf
from rest_framework.authtoken.models import Token # generates/ get token for authenticated user
from rest_framework.decorators import api_view, permission_classes # some usefull decorators
from rest_framework.permissions import (
    AllowAny, 
    IsAuthenticatedOrReadOnly, 
    IsAuthenticated,
) # allowing all users to interact with the view

from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_202_ACCEPTED,
    HTTP_204_NO_CONTENT, HTTP_500_INTERNAL_SERVER_ERROR
) # Some Basic HTTP responses
from rest_framework.response import Response # sending json response

# Some required imports
from .models import * 
from .serializers import *



@csrf_exempt
@api_view(['POST', ])
@permission_classes((AllowAny,))
def auth(request):
    try:
        username = request.data.get("username")
        password = request.data.get("password")
        if username is None or password is None:
            return Response({"error": True, "message": "Please provide both username and password"}, status=HTTP_400_BAD_REQUEST)
        user = authenticate(username=username, password=password)
        if not user:
            return Response({"error": True, "message": "Invalid Credentials"}, status=HTTP_404_NOT_FOUND)
        
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "auth": True}, status=HTTP_200_OK)
    
    except Event.DoesNotExist as err:
        return Response({"error": True, "message": "event does not exists"}, status=HTTP_404_NOT_FOUND)

    except Exception as err:
        return Response({"error": True, "message": err}, status=HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(["GET", ])
@permission_classes((AllowAny,))
def welcome(request):
    try:
        fetch = request.query_params.get('fetch', -1)
        eventId = request.query_params.get('eventId', -1)
        if eventId == -1 and fetch == -1:
            return Response("Welcome To API IGConnect API", status=HTTP_200_OK)
        
        if fetch == 'events':
            events = Event.objects.all()
            events_serialized = EventSerializer(events, many=True)
            return Response(events_serialized.data, status=HTTP_200_OK)

        event = Event.objects.get(id=eventId)
        if fetch == "registrations":
            registration = event.registration.all()
            reg_serialized = RegistrationSerializer(registration, many=True)
            return Response(reg_serialized.data, status=HTTP_200_OK)
        
        elif fetch == "prizes":
            prize = event.prize.all()
            prize_serialized = PrizeSerializer(prize, many=True)
            return Response(prize_serialized.data, status=HTTP_200_OK)
        
        elif fetch == "timelines":
            timeline = event.timeline.all()
            timeline_serialized = TimelineSerializer(timeline, many=True)
            return Response(timeline_serialized.data, status=HTTP_200_OK)      
             
    except Event.DoesNotExist as err:
        return Response({"error": True, "message": "event does not exists"}, status=HTTP_404_NOT_FOUND)

    except Exception as err:
        print(err)
        return Response({"error": True, "message": "system error"}, status=HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(["GET", ])
@permission_classes((AllowAny,))
def allevents(request):
    try:
        date_choice = ['eq', 'lt', 'gt', 'lte', 'gte']
        date = request.query_params.get('date', '') #== eq, < lt, > gt, <= lte, >= gte to today's date
        if date not in date_choice:
            return Response({
                "error": True, 
                "message": "date must contain any of these: "+", ".join(date_choice)
                }, status=HTTP_400_BAD_REQUEST)
                
        events = Event.getAccToDate(date)
        events_serialized = EventSerializer(events, many=True)        
        return Response(events_serialized.data, status=HTTP_200_OK)
        
    except Event.DoesNotExist as err:
        return Response({"error": True, "message": "event does not exists"}, status=HTTP_404_NOT_FOUND)

    except Exception as err:
        print(err)
        return Response({"error": True, "message": "system error"}, status=HTTP_500_INTERNAL_SERVER_ERROR)



@csrf_exempt
@api_view(["POST", "GET", "PUT", "DELETE"])
@permission_classes((IsAuthenticatedOrReadOnly, ))
def event(request):
    try:
        if request.method == "POST":
            serializer = EventSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"created": "OK"}, status=HTTP_201_CREATED)

            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        
        else:
            eventId = request.query_params.get("eventId", -1)
            if(eventId == -1):
                return Response({"error": True, "message": 'parameter eventId not passed'}, status=HTTP_400_BAD_REQUEST)
            
            event = Event.objects.get(id = eventId)
            if request.method == "GET":
                event_serialized = EventSerializer(event)
                return Response(event_serialized.data, status=HTTP_200_OK)
            
            elif request.method == "PUT":
                event_serialized = EventSerializer(event, data=request.data)
                if event_serialized.is_valid():
                    event_serialized.save()
                    return Response({"message": "event update success"}, status=HTTP_202_ACCEPTED)

                return Response({"error": True, "message": event_serialized.errors}, status=HTTP_400_BAD_REQUEST)
            
            elif request.method == "DELETE":
                event.delete()
                return Response({"message": "event delete success"}, status=HTTP_204_NO_CONTENT)

    except Event.DoesNotExist as err:
        return Response({"error": True, "message": "event does not exists"}, status=HTTP_404_NOT_FOUND)

    except Exception as err:
        print(err)
        return Response({"error": True, "message": err}, status=HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(["POST", "GET", "PUT", "DELETE"])
@permission_classes((IsAuthenticatedOrReadOnly, ))
def timeline(request):
    try:
        if request.method == "POST":
            serializer = TimelineSerializer(data = request.data)
            print(serializer)
            if serializer.is_valid():
                serializer.save()
                return Response({"created": "OK"}, status=HTTP_201_CREATED)
            
            return Response({"error": True, "message" : serializer.errors}, status=HTTP_400_BAD_REQUEST)
        
        else:
            timelineId = request.query_params.get('timelineId', -1)
            timeline = Timeline.objects.get(id = timelineId)
            if request.method == "GET":
                timeline_serialized = TimelineSerializer(timeline)
                return Response(timeline_serialized.data, status=HTTP_200_OK)

            elif request.method == "PUT":
                timeline_serialized = TimelineSerializer(timeline, request.data)
                if timeline_serialized.is_valid():
                    timeline_serialized.save()
                    return Response({"message": "timeline update success"}, status=HTTP_202_ACCEPTED)
                
                else:
                    return Response({"error": True, "message": timeline_serialized.errors}, status=HTTP_400_BAD_REQUEST)

            elif request.method == "DELETE":
                timeline.delete()
                return Response({"message": "timeline delete success"}, status=HTTP_204_NO_CONTENT)

    except Timeline.DoesNotExist as err:
        return Response({"error": True, "message": "timeline does not exists"}, status=HTTP_404_NOT_FOUND)

    except Exception as err:
        print(err)
        return Response({"error": True, "message": "system error"}, status=HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(["POST", "GET", "PUT", "DELETE"])
@permission_classes((IsAuthenticatedOrReadOnly, ))
def prize(request):
    try:
        if request.method == "POST":
            serializer = PrizeSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"created": "OK"}, status=HTTP_201_CREATED)

            return Response({"error": True, "message": serializer.errors}, status=HTTP_400_BAD_REQUEST)
        else:
            prizeId = request.query_params.get('prizeId', -1)
            prize = Prize.objects.get(id=prizeId)
            
            if request.method == "GET":
                prize_serialized = PrizeSerializer(prize)
                return Response(prize_serialized.data, status=HTTP_200_OK)

            elif request.method == "PUT":
                prize_serialized = PrizeSerializer(prize, data=request.data)
                if prize_serialized.is_valid():
                    prize_serialized.save()
                    return Response({"message": "prize update success"}, status=HTTP_202_ACCEPTED)
                
                else:
                    return Response({"error": True, "message": prize_serialized.errors}, status=HTTP_400_BAD_REQUEST)

            elif request.method == "DELETE":
                prize.delete()
                return Response({"message": "prize delete success"}, status=HTTP_204_NO_CONTENT)

    except Prize.DoesNotExist as err:
        return Response({"message": "prize requested does not exists"}, status=HTTP_404_NOT_FOUND)

    except Exception as err:
        print(err)
        return Response({"error": True, "message": "system error"}, status=HTTP_500_INTERNAL_SERVER_ERROR)

@csrf_exempt
@api_view(["POST", "GET", "PUT", "DELETE"])
@permission_classes((IsAuthenticated, ))
def registration(request):
    try:
        if request.method == "POST":
            serializer = RegistrationSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"created": "OK"}, status=HTTP_201_CREATED)

            return Response({"error": True, "message": serializer.errors}, status=HTTP_400_BAD_REQUEST)

        else:
            regId = request.query_params.get('regId', -1)
            registration = Registration.objects.get(id=regId)
            if request.method == "GET":
                reg_serialized = RegistrationSerializer(registration)
                return Response(reg_serialized.data, status=HTTP_200_OK)

            elif request.method == "PUT":
                reg_serialized = RegistrationSerializer(registration, data=request.data)
                if reg_serialized.is_valid():
                    reg_serialized.save()
                    return Response({"message": "registration update success"}, status=HTTP_202_ACCEPTED)
                
                else:
                    registration.delete()
                    return Response({"error": True, "message": reg_serialized.errors}, status=HTTP_400_BAD_REQUEST)

            elif request.method == "DELETE":
                registration.delete()
                return Response({"message": "registration delete success"}, status=HTTP_204_NO_CONTENT)

    except Registration.DoesNotExist as err:
        return Response({"message": "registeration requested does not exists"}, status=HTTP_404_NOT_FOUND)
        
    except Exception as err:
        return Response({"error": True, "message": err}, status=HTTP_500_INTERNAL_SERVER_ERROR)

                