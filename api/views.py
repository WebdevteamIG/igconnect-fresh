from django.contrib.auth import authenticate # to manually authenticate user
from django.views.decorators.csrf import csrf_exempt # to use POST req without csrf
from rest_framework.authtoken.models import Token # generates/ get token for authenticated user
from rest_framework.decorators import api_view, permission_classes # some usefull decorators
from rest_framework.permissions import (
    AllowAny, 
    IsAuthenticatedOrReadOnly, 
    IsAuthenticated,
) # allowing all users to interact with the view

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

# Some required imports
from .models import * 
from .serializers import *

@csrf_exempt
@api_view(["POST", "GET", "PUT", "DELETE"])
@permission_classes((IsAuthenticatedOrReadOnly, ))
def user(request):
    userId = request.query_params.get('userId', -1)
    try:
        if request.method == "POST":
            serializer = UserSerializer(data=request.data)
            if serializers.is_valid():
                serializer.save()
                return Response({"message": "create success"}, status=HTTP_201_CREATED)
            
            return Response({"error": True, "message": serializer.errors}, status=HTTP_400_BAD_REQUEST)
        
        if userId == -1:
            return Response({"errors": True, "message": "required a valid userId as parameter"}, status=HTTP_400_BAD_REQUEST)

        user = User.objects.get(id = userId)
        if request.method == "GET":
            serialized = UserSerializer(user)
            return Response(serialized.data, status=HTTP_200_OK)
        
        elif request.method == "PUT":
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "update success"}, status=HTTP_202_ACCEPTED)
            
            return Response({"error": True, "message": serializer.errors}, status=HTTP_400_BAD_REQUEST)
        
        else:
            user.delete()
            return Response({"message": "user delete success"}, status=HTTP_204_NO_CONTENT)

    except User.DoesNotExist as err:
        return Response({"error": True, "message": "user for userId = {} doesnot exists".format(userId)})

    except Exception as err:
        print(err)
        return Response({"error": True, "message": "System Error"}, status=HTTP_500_INTERNAL_SERVER_ERROR)


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
            registration = event.allRegistrations.all()
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
                return Response({"message" : "create success"}, status=HTTP_201_CREATED)

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
                event_serialized = EventSerializer(event, data=request.data, partial=True)
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
            if serializer.is_valid():
                serializer.save()
                return Response({"message" : "create success"}, status=HTTP_201_CREATED)
            
            return Response({"error": True, "message" : serializer.errors}, status=HTTP_400_BAD_REQUEST)
        
        else:
            timelineId = request.query_params.get('timelineId', -1)
            if timelineId == -1:
                return Response({"error": True, "message": "please pass timelineId as a query parameter"}, status=HTTP_400_BAD_REQUEST)

            timeline = Timeline.objects.get(id = timelineId)
            if request.method == "GET":
                timeline_serialized = TimelineSerializer(timeline)
                return Response(timeline_serialized.data, status=HTTP_200_OK)

            elif request.method == "PUT":
                timeline_serialized = TimelineSerializer(timeline, request.data, partial=True)
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
                return Response({"message" : "create success"}, status=HTTP_201_CREATED)

            return Response({"error": True, "message": serializer.errors}, status=HTTP_400_BAD_REQUEST)
        else:
            prizeId = request.query_params.get('prizeId', -1)
            prize = Prize.objects.get(id=prizeId)
            
            if request.method == "GET":
                prize_serialized = PrizeSerializer(prize)
                return Response(prize_serialized.data, status=HTTP_200_OK)

            elif request.method == "PUT":
                prize_serialized = PrizeSerializer(prize, data=request.data, partial=True)
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
@permission_classes((AllowAny, ))
def registration(request):
    try:
        if request.method == "POST":
            userNum = request.data.get('userNumber', '')
            event = request.data.get('event', -1)
            reg = Registration.objects.filter(userNumber=userNum, event__id=event)
            if len(reg) > 0:
                return Response({"error": True, "message": "registration with this mobile number exists already"})

            serializer = RegistrationSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message" : "create success"}, status=HTTP_201_CREATED)

            return Response({"error": True, "message": serializer.errors}, status=HTTP_400_BAD_REQUEST)

        else:
            regId = request.query_params.get('regId', -1)
            registration = Registration.objects.get(id=regId)
            if request.method == "GET":
                reg_serialized = RegistrationSerializer(registration)
                return Response(reg_serialized.data, status=HTTP_200_OK)

            elif request.method == "PUT":
                reg_serialized = RegistrationSerializer(registration, data=request.data, partial=True)
                if reg_serialized.is_valid():
                    reg_serialized.save()
                    return Response({"message": "registration update success"}, status=HTTP_202_ACCEPTED)
                
                else:
                    return Response({"error": True, "message": reg_serialized.errors}, status=HTTP_400_BAD_REQUEST)

            elif request.method == "DELETE":
                registration.delete()
                return Response({"message": "registration delete success"}, status=HTTP_204_NO_CONTENT)

    except Registration.DoesNotExist as err:
        return Response({"message": "registeration requested does not exists"}, status=HTTP_404_NOT_FOUND)
        
    except Exception as err:
        print(err)
        return Response({"error": True, "message": "internal server error"}, status=HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(["POST", "GET", "PUT", "DELETE"])
@permission_classes((IsAuthenticated, ))
def addMedia(request):
    mediaId = request.query_params.get('mediaId', -1)
    try:
        if request.method == "POST":
            serializer = EventMediaSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message" : "create success"}, status=HTTP_201_CREATED)

            return Response({"error": True, "message": serializer.errors}, status=HTTP_400_BAD_REQUEST)

        else:
            media = EventMedia.objects.get(id=mediaId)
            if request.method == "GET":
                serialized = EventMediaSerializer(media)
                return Response(serialized.data, status=HTTP_200_OK)

            elif request.method == "PUT":
                serialized = EventMediaSerializer(media, data=request.data, partial=True)
                if serialized.is_valid():
                    serialized.save()
                    return Response({"message": "event media file update success"}, status=HTTP_202_ACCEPTED)
                
                else:
                    return Response({"error": True, "message": serialized.errors}, status=HTTP_400_BAD_REQUEST)

            elif request.method == "DELETE":
                media.delete()
                return Response({"message": "event media file delete success"}, status=HTTP_204_NO_CONTENT)

    except Registration.DoesNotExist as err:
        return Response({"message": "media file with id = {} requested does not exists".format(mediaId)}, status=HTTP_404_NOT_FOUND)
        
    except Exception as err:
        return Response({"error": True, "message": err}, status=HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(["GET", ])
@permission_classes((AllowAny, ))
def mySubmission(request):
    try:
        userNum = request.query_params.get('userNumber', '')
        event = request.query_params.get('event', -1)
        submission = Submission.objects.filter(user__userNumber=userNum, event__id=event)
        serialized = SubmissionSerializer(submission, many=True)
        return Response({"message": serialized.data}, status=HTTP_200_OK)
    
    except Exception as err:
        print(err)
        return Response({"error": True, "message": "internal server error"}, status=HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(["POST", "PUT", "DELETE"])
@permission_classes((AllowAny, ))
def submission(request):
    id = request.query_params.get('id', -1)
    try:
        if request.method == "POST":
            request.data._mutable = True
            userNumber = request.data.get('userNumber', '')[-10:]
            event = request.data.get('event', -1)
            reg = TimelineRegistration.objects.get(registration__userNumber=userNumber, timeline__id=event)
            request.data['user'] = str(reg.registration.id)
            submission = Submission.objects.filter(event__id=event, user__id=request.data['user'])
            if len(submission) != 0:
                return Response({"error": True, "message": "submission for the user number already exists"}, status=HTTP_409_CONFLICT)

            serializer = SubmissionSerializer(data = request.data)

            if serializer.is_valid():
                serializer.save()
                return Response({"message": "submission create success"}, status=HTTP_201_CREATED)

            return Response({"error": True, "message": serializer.errors}, status=HTTP_400_BAD_REQUEST)

        else:
            submission = Submission.objects.get(id=id)
            if request.method == "PUT":
                serialized = SubmissionSerializer(submission, data=request.data, partial=True)
                if serialized.is_valid():
                    serialized.save()
                    return Response({"message": "submission update success"}, status=HTTP_202_ACCEPTED)
                
                else:
                    return Response({"error": True, "message": serialized.errors}, status=HTTP_400_BAD_REQUEST)

            elif request.method == "DELETE":
                submission.delete()
                return Response({"message": "submission delete success"}, status=HTTP_204_NO_CONTENT)

    except TimelineRegistration.DoesNotExist as err:
        return Response({"message": "this mobile number is not registered for this timeline of the event"}, status=HTTP_404_NOT_FOUND)

    except Submission.DoesNotExist:
        return Response({"message": "submission requested does not exits"}, status=HTTP_404_NOT_FOUND)
             

    except Exception as err:
        print(err)
        return Response({"error": True, "message": "internal server error"}, status=HTTP_500_INTERNAL_SERVER_ERROR)



@csrf_exempt
@api_view(["POST", "GET", "PUT", "DELETE"])
@permission_classes((AllowAny, ))
def team(request):
    id = request.query_params.get('id', -1)
    try:
        if request.method == "POST":
            userNumber = request.query_params.get('userNumber', '')[-10:]
            event = request.data.get('event', '')
            if(userNumber == ''):
                return Response({"error": True, "message": "pass a valid mobile number."})

            reg = Registration.objects.get(userNumber=userNumber, event__id=event)
            if len(reg) == 0:
                return Response({"error": True, "message": "no registration for this mobile number exists, please first register for the event."})
            
            teamName = request.data.get('teamname', '')
            team = Team.objects.filter(event__id=event, teamname=teamName)
            if len(team) != 0:
                return Response({"error": True, "message": "this team name is already taken"})

            request.data['leader'] = reg.userNumber
            serializer = TeamSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "team create success"}, status=HTTP_201_CREATED)

            return Response({"error": True, "message": serializer.errors}, status=HTTP_400_BAD_REQUEST)

        else:
            team = Team.objects.get(id=id)
            if request.method == "GET":
                serialized = TeamSerializer(submission)
                return Response(serialized.data, status=HTTP_200_OK)

            elif request.method == "PUT":
                serialized = TeamSerializer(submission, data=request.data, partial=True)
                if serialized.is_valid():
                    serialized.save()
                    return Response({"message": "team update success"}, status=HTTP_202_ACCEPTED)
                
                else:
                    return Response({"error": True, "message": serialized.errors}, status=HTTP_400_BAD_REQUEST)

            elif request.method == "DELETE":
                submission.delete()
                return Response({"message": "team delete success"}, status=HTTP_204_NO_CONTENT)

    except Registration.DoesNotExist as err:
        return Response({"message": "team with id = {} requested does not exists".format(id)}, status=HTTP_404_NOT_FOUND)
        
    except Exception as err:
        return Response({"error": True, "message": err}, status=HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(["GET", ])
@permission_classes((AllowAny, ))
def joinTeam(request):
    try:
        teamName = request.query_params.get('teamName', '')
        userNumber = request.query.get('userNumber', '')
        event = request.data.get('eventId', -1)
        missing = []
        if teamName == '':
            missing.append('team name')
        
        if userNumber == '':
            missing.append('user number')
        
        if event == -1:
            missing.append('event id')

        if len(missing) > 0:
            return Response({"error": True, "message": 'please pass valid '+', '.join(missing)}, status=HTTP_400_BAD_REQUEST)
        
        registration = Registration.objects.get(event__id=event, userNumber=userNumber)
        team = Team.objects.get(event__id=event, teamname=teamName)
        registration.team = team
        registration.save()
        return Response({"message": "team add success"}, status=HTTP_201_CREATED)

    except Registration.DoesNotExist :
        return Response({"error": True, "message": "requested registration doesnot exits"}, status=HTTP_404_NOT_FOUND)
    
    except Team.DoesNotExist :
        return Response({"error": True, "message": "requested team doesnot exits"}, status=HTTP_404_NOT_FOUND)
    
    except Exception:
        return Response({"error": True, "message": "internal server error"}, status=HTTP_500_INTERNAL_SERVER_ERROR)

@csrf_exempt
@api_view(["GET", ])
@permission_classes((AllowAny, ))
def registerTimeline(request):
    try:
        timelineId = request.query_params.get('timelineId', '')
        userNumber = request.query_params.get('userNumber', '')[-10:]
        event = request.query_params.get('eventId', -1)

        missing = []
        if timelineId == '':
            missing.append('team name')
        
        if userNumber == '':
            missing.append('user number')
        
        if event == -1:
            missing.append('event id')

        if len(missing) > 0:
            return Response({"error": True, "message": 'please pass valid '+', '.join(missing)}, status=HTTP_400_BAD_REQUEST)

        timeline = Timeline.objects.get(id=timelineId)
        registration = Registration.objects.get(event__id=event, userNumber=userNumber)
        regTimeline, isCreate = TimelineRegistration.objects.get_or_create(registration=registration, timeline=timeline)
        if isCreate:
            return Response({"message": "team add success"}, status=HTTP_201_CREATED)
        
        else:
            return Response({"message": "allready registered for this timeline of event"}, status=HTTP_409_CONFLICT)

    except Registration.DoesNotExist :
        return Response({"error": True, "message": "requested registration doesnot exits"}, status=HTTP_404_NOT_FOUND)
    
    except Timeline.DoesNotExist :
        return Response({"error": True, "message": "requested timeline doesnot exits"}, status=HTTP_404_NOT_FOUND)
    
    except Exception as err:
        print(err)
        return Response({"error": True, "message": "internal server error"}, status=HTTP_500_INTERNAL_SERVER_ERROR)

