from django.views.generic import ListView
from django.http import Http404
from django.urls import reverse
from django.shortcuts import render, redirect
from . import models


class HomeView(ListView):  # core폴더의 url에도 넣어뒀음

    """ HomeView Definition """

    model = models.Room
    paginate_by = 10  # ListView 관련사항 ccv.co.uk확인하면 잘 정리되어있음
    paginate_orphans = 5
    ordering = "created"
    context_object_name = "rooms"


def room_detail(request, pk):  # pk가 room id이고 url 뒤에 붙겍되는건지
    try:
        room = models.Room.objects.get(pk=pk)  # 데이터베이스에서 룸 정보를 가져오기 위해
        return render(request, "rooms/detail.html", {"room": room})
    except models.Room.DoesNotExist:  # 예외처리하기 위해서, pk넘버에 없는걸 주소에 넣으면 이쪽으로 처리되도록
        # return redirect(reverse("core:home"))  # url대신 reverse 써서 하는걸 추천, 홈으로 보내주는거
        raise Http404()  # 오류는 return이 아니라 raise사용 #404띄우면 따로 저장안하니까 이렇게 써도 괜찮지
        # setting.py 에서 DEBUG = False, ALLOWED_HOST = "*" 해야지만 이 templates에 있는 404.html을 볼 수 있다
