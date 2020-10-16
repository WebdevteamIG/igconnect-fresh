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
    try:
        fetch = request.query_params.get('fetch', -1)
        if fetch == 'events':
            events = Event.objects.all()
            events_serialized = EventSerializer(events, many=True)
            return Response(events_serialized, status=HTTP_200_OK)

        eventId = request.query_params.get('eventId', -1)
        event = Event.objects.get(id=eventId)
        if fetch == "registrations":
            registration = event.registration.objects.all()
            reg_serialized = RegistrationSerializer(registration, many=True)
            return Response(reg_serialized, status=HTTP_200_OK)
        
        elif fetch == "prizes":
            prize = event.prize.objects.all()
            prize_serialized = PrizeSerializer(prize, many=True)
            return Response(prize_serialized, status=HTTP_200_OK)
        
        elif fetch == "timelines":
            timeline = event.timeline.objects.all()
            timeline_serialized = TimelineSerializer(timeline, many=True)
            return Response(timeline_serialized, status=HTTP_200_OK)
        
        else:        
            return Response("Welcome To API IGConnect API", status=HTTP_200_OK)
    
    except Event.DoesNotExist as err:
        return Response({"error": True, "message": "event does not exists"}, status=HTTP_404_NOT_FOUND)

    except Exception as err:
        return Response({"error": True, "message": json.dump(err)})


@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def allevents(request):
    try:
        date_choice = ['eq', 'lt', 'gt', 'lte', 'gte']
        date = request.query_params.get('date', -1) #== eq, < lt, > gt, <= lte, >= gte to today's date
        if date not in date_choice:
            return Response({
                "error": True, 
                "message": "date must contain any of these: "+", ".join(date_choice)
                }, status=HTTP_400_BAD_REQUEST)
                
        events = Event.getAccToDate(date)
        events_serialized = EventSerializer(events, many=True)
        return Response(events_serialized, status=HTTP_200_OK)
        
    except Event.DoesNotExist as err:
        return Response({"error": True, "message": "event does not exists"}, status=HTTP_404_NOT_FOUND)

    except Exception as err:
        return Response({"error": True, "message": json.dump(err)})



@csrf_exempt
@api_view(["POST", "GET", "PUT", "DELETE"])
@permission_classes((IsAuthenticatedOrReadOnly))
def event(request):
    try:
        if request.method == "POST":
            serializer = EventSerializer(data = request.data)
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
                return Response(event_serialized, status=HTTP_200_OK)
            
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
        return Response({"error": True, "message": json.dump(err)})


@csrf_exempt
@api_view(["POST", "GET", "PUT", "DELETE"])
@permission_classes((IsAuthenticatedOrReadOnly))
def timeline(request, eventId):
    try:
        event = Event.objects.get(id = eventId)
        if request.method == "POST":
            serializer = TimelineSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"created": "OK"}, status=HTTP_201_CREATED)
            
            return Response({"error": True, "message" : serializer.errors}, status=HTTP_400_BAD_REQUEST)
        
        else:
            timelineId = request.query_params.get('timelineId', -1)
            if request.method == "GET":
                timeline = Timeline.objects.get(id = timelineId)
                timeline_serialized = TimelineSerializer(timeline)
                return Response(timeline_serialized, status=HTTP_200_OK)

            elif request.method == "PUT":
                timeline = Timeline.objects.get(id = timelineId)
                timeline_serialized = TimelineSerializer(timeline)
                if timeline_serialized.is_valid():
                    timeline_serialized.save()
                    return Response({"message": "event update success"}, status=HTTP_202_ACCEPTED)
                
                else:
                    return Response({"error": True, "message": timeline_serialized.errors}, status=HTTP_400_BAD_REQUEST)

            elif request.method == "DELETE":
                timeline = Timeline.objects.get(id = timelineId)
                timeline.delete()
                return Response({"message": "event delete success"}, status=HTTP_204_NO_CONTENT)

    except Event.DoesNotExist as err:
        return Response({"error": True, "message": "such timeline does not exists"}, status=HTTP_404_NOT_FOUND)

    except Exception as err:
        return Response({"error": True, "message": json.dump(err)})


@csrf_exempt
@api_view(["POST", "GET", "PUT", "DELETE"])
@permission_classes((IsAuthenticatedOrReadOnly))
def prize(request, eventId):
    try:
        event = Event.objects.get(id = eventId)
        if request.method == "POST":
            serializer = PrizeSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"created": "OK"}, status=HTTP_201_CREATED)

            return Response({"error": True, "message": serializer.errors}, status=HTTP_400_BAD_REQUEST)
        else:
            prizeId = request.query_params.get('prizeId', -1)
            if request.method == "GET":
                prize = Prize.objects.get(id=prizeId)
                prize_serialized = PrizeSerializer(prize)
                return Response(prize_serialized, status=HTTP_200_OK)

            elif request.method == "PUT":
                prize = Prize.objects.get(id = prizeId)
                prize_serialized = PrizeSerializer(prize)
                if prize_serialized.is_valid():
                    prize_serialized.save()
                    return Response({"message": "event update success"}, status=HTTP_202_ACCEPTED)
                
                else:
                    return Response({"error": True, "message": prize_serialized.errors}, status=HTTP_400_BAD_REQUEST)

            elif request.method == "DELETE":
                prize = Prize.objects.get(id = prizeId)
                prize.delete()
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
            serializer = RegistrationSerializer(data = request.data)

            if serializer.is_valid():
                serializer.save()
                return Response({"created": "OK"}, status=HTTP_201_CREATED)

            return Response({"error": True, "message": serializer.errors}, status=HTTP_400_BAD_REQUEST)
        else:
            regId = request.query_params.get('registrationId', -1)
            registration = Registration.objects.get(id=regId)
            if request.method == "GET":
                reg_serialized = RegistrationSerializer(registration)
                return Response(reg_serialized, status=HTTP_200_OK)

            elif request.method == "PUT":
                reg_serialized = RegistrationSerializer(registration)
                if reg_serialized.is_valid():
                    reg_serialized.save()
                    return Response({"message": "registration update success"}, status=HTTP_202_ACCEPTED)
                
                else:
                    registration.delete()
                    return Response({"error": True, "message": reg_serialized.errors}, status=HTTP_400_BAD_REQUEST)

            elif request.method == "DELETE":
                return Response({"message": "event delete success"}, status=HTTP_204_NO_CONTENT)
    except Event.DoesNotExist as err:
        return Response({"message": "event does not exists"}, status=HTTP_404_NOT_FOUND)
    except Exception as err:
        return Response({"error": True, "message": json.dump(err)})

                