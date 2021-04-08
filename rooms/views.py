from django.shortcuts import render
from . import models


def all_rooms(request):
    all_rooms = models.Room.objects.all()
    return render(request, "rooms/home.html", context={"rooms": all_rooms})
    # render 통해서 html을 가져오는데, context를 이용해서 여기있는 변수를 html에서 사용할 수 있음.
