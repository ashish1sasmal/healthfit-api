from django.shortcuts import redirect, render

# Create your views here.
import uuid

from app.models import ChatRoom
from .constants import *
from django.contrib.auth.decorators import login_required

import uuid
from datetime import datetime
from django.http import JsonResponse
from django.contrib.auth import get_user_model
User = get_user_model()

@login_required
def startRoom(request):
    room_id = str(uuid.uuid4().hex)[:8]
    room = ChatRoom(admin=request.user, room_id=room_id)
    room.save()
    room.members.add(request.user)
    room.save()
    print("[ Chatroom created ]")
    return redirect("app:enterRoom", room_id=room_id)

@login_required
def enterRoom(request, room_id):
    try:
        print(f"room_id : {room_id}")
        room = ChatRoom.objects.get(room_id=room_id)
        if request.user not in room.members.all():
            return redirect("app:waitRoom", room_id=room_id)
        room.members.add(request.user)
        room.last_active = datetime.now()
        room.save()
        context = {
            "room": room,
            "messages": room.message_room.all()
        }
        return render(request, "app/sender2.html", context=context)
    except ChatRoom.DoesNotExist as err:
        print(str(err))
        return JsonResponse({})


    
@login_required
def deleteRoom(request, room_id):
    try:
        room = ChatRoom.objects.get(room_id=room_id)
        room.delete()
        return JsonResponse({"result": True})
    except Exception as err:
        print(str(err))
        return JsonResponse({"result": False})