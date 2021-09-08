import json
import datetime

from users.permissions import IsProfileFilled
from users.models import User
from users.models import Team
from uuid import uuid4
from .serializers import EventSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.http.response import JsonResponse
from .models import Event
from users.serializers import TeamSerializer


def is_time_between(begin_time, end_time, check_time=None):
    check_time = check_time or datetime.utcnow().time()
    if begin_time < end_time:
        return check_time >= begin_time and check_time <= end_time
    else:
        return check_time >= begin_time or check_time <= end_time

class EventListView(APIView):
  def get(self, request):
    events = Event.objects.all()
    serializer = EventSerializer(events, many=True)
    return JsonResponse({"events": serializer.data, "success": True}, status=200)

class EventDetailVIew(APIView):

  def get(self, request,event_code):
    print(event_code)
    try:
      event =  Event.objects.get(event_code=event_code)
      serializer = EventSerializer(event)
      teams = TeamSerializer(event.participants, many=True)
      # serializer.data['participants'] = teams.data
      data = {
        **serializer.data,
        "participants": teams.data,
      }
      return JsonResponse({"success": True, "event": data}, status=200)
    except Event.DoesNotExist:
      return JsonResponse({"detail": "Event Doesn't Exists", "success": False}, status=400)
    
class EventRegiterView(APIView):
  permission_classes = [IsAuthenticated, IsProfileFilled]

  def post(self, request):
    # def update_criteria(user: User, event: Event) -> User:
    #   user_criteria = json.loads(user.criteria)
    #   user_criteria[str(event.day)] = True
    #   user.criteria = json.dumps(user_criteria)
    #   return user
    
    def check_event_clashes(user: User, event: Event) -> list:
      participations = user.teams.all()
      for p in participations:
        e = p.event
        print(e.start, e.end, event.start, event.day == e.day)
        if event.day == e.day and is_time_between(e.start, e.end, event.start):
          return [e,True]
      return [None, False]

    user = request.user
    event_code = request.data['event_code']
    event = None
    print(event_code)
    try:
      event = Event.objects.get(event_code=event_code)
    except Event.DoesNotExist:
      return JsonResponse({"detail": "Event Doesn't Exists", "success": False}, status=400)


    if event.seats == event.max_seats:
      return JsonResponse({"detail": "Event Doesn't have Seats Left!", "success": False}, status=400)

    e = user.teams.filter(event=event).count()
    if e > 0:
      return JsonResponse({"detail": "You have Already Registered For this Event", "success": False}, status=400)
    
    # checking time clashes with other events
    [ec, result] = check_event_clashes(user, event)
    if result:
      return JsonResponse({"detail": f"This Event Clashes with the {ec.title} Event({ec.start} - {ec.end})", "success": False}, status=400)
    
    if event.team_size == 1:
      # Event is Solo Event
         
      # create a Team of One
      t = Team()
      t.event = event
      t.team_name = user.roll_no
      t.save()
      t.members.add(user)
      
      # add to moneyOwed
      user.money_owed += event.entry_fee

      # update criteria
      # user = update_criteria(user, event)

      # Update Event seats
      # now changed to after team verified
      # event.seats += 1

      try:
        t.save()
        # event.save()
        user.save()
        team_serializer = TeamSerializer(t)
        print(team_serializer.data)
        # event_serializer = EventSerializer(event)
        return JsonResponse({"detail": "Event Registered Sucessfully!", "team": team_serializer.data, "success": True}, status=200)
      except:
        t.delete()
        return JsonResponse({"detail": "Something Went Wrong!", "success": False}, status=400)

    else:
      # Event is Team Event
      
      team_name = request.data['team_name']
      members = request.data["members"]

      if user.roll_no not in members:
        members.add(user.roll_no)

      if event.is_team_size_strict and len(members) != event.team_size:        
        return JsonResponse({"detail": f"Event Has a Strict Team Size of {event.team_size}", "success": False}, status=400)

      if len(set(members)) != len(members):
        return JsonResponse({"detail": "Team have Repeated Members, Please ensure they are Unique!", "success": False}, status=400)

      t = Team()
      t.event = event
      t.team_name = team_name
      t.save()

      
      for m in members:
        try:
          u = User.objects.get(roll_no=m)
          t.members.add(u)
        except User.DoesNotExist:
          t.delete()
          return JsonResponse({"detail": "Roll Number is Not Valid or Doesn't Exists", "success": False}, status=400)
        
      for m in t.members.all():
        if not m.has_filled_profile or not m.is_phone_no_verified:
          t.delete()
          return JsonResponse({"detail": "Some Member(s) have not filled their Profile", "success": False}, status=400)
      
      # add to moneyOwed
      user.money_owed += event.entry_fee

      # Update Event seats
      # now changed to after team verified
      # event.seats += 1
      
      try:
        t.save()
        event.save()
        # update criteria for members
        # print(t.members.all())
        # for m in t.members.all():
        #   if m.roll_no == user.roll_no: continue
        #   m = update_criteria(m, event)
        #   m.save()

        # user = update_criteria(user, event)
        user.save()
        team_serializer = TeamSerializer(t)
        return JsonResponse({"detail": "Event Registered Sucessfully!", "team": team_serializer.data, "success": True}, status=200)
      except:
        t.delete()
        return JsonResponse({"detail": "Something Went Wrong!",  "success": False}, status=400)


class EventUnregister(APIView):
  permission_classes = [IsAuthenticated]
  def post(self, request):
    user = request.user
    team_code = request.data["team_code"]


    teams = user.teams.filter(team_code=team_code)
    if teams.count() < 1:
      return JsonResponse({"detail": "You have not Registered For the Event", "success": False}, status=400)
    
    team = teams.first()
    if team.is_paid:
      return JsonResponse({"detail": "You have Already Paid for the Event", "success": False}, status=400)
          
    try:
      team.delete()
      return JsonResponse({"detail": "Participation Successfully Deleted!", "success": True}, status=200)
    except:
      return JsonResponse({"detail": "Something Went Wrong!", "success": False}, status=400)


    