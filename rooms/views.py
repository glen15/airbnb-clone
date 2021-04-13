from django.views.generic import ListView, DetailView
from django.shortcuts import render
from django.urls import reverse
from . import models

# 밑에 둘은 function기반으로할때 사용
# from django.http import Http404
# from django.shortcuts import render, redirect


class HomeView(ListView):  # core폴더의 url에도 넣어뒀음

    """ HomeView Definition """

    model = models.Room
    paginate_by = 10  # ListView 관련사항 ccv.co.uk확인하면 잘 정리되어있음
    paginate_orphans = 5
    ordering = "created"
    context_object_name = "rooms"


# class 기반 views
class RoomDetail(
    DetailView
):  # DetailView 사용하면 django가 기본적으로 url argument로 pk를 찾는다 urls.py에 있는 int:pk

    """ RoomDetail Definition """

    model = models.Room


# function 기반으로 views 만든 것
# def room_detail(request, pk):  # pk가 room id이고 url 뒤에 붙겍되는건지
#     try:
#         room = models.Room.objects.get(pk=pk)  # 데이터베이스에서 룸 정보를 가져오기 위해
#         return render(request, "rooms/detail.html", {"room": room})
#     except models.Room.DoesNotExist:  # 예외처리하기 위해서, pk넘버에 없는걸 주소에 넣으면 이쪽으로 처리되도록
#         # return redirect(reverse("core:home"))  # url대신 reverse 써서 하는걸 추천, 홈으로 보내주는거
#         raise Http404()  # 오류는 return이 아니라 raise사용 #404띄우면 따로 저장안하니까 이렇게 써도 괜찮지
#         # setting.py 에서 DEBUG = False, ALLOWED_HOST = "*" 해야지만 이 templates에 있는 404.html을 볼 수 있다


def search(request):
    city = request.GET.get("city")
    city = str.capitalize(city)  # 데이터베이스 안에는 첫번째가 대문자로 되어있어서 거기에 맞게 변경
    return render(
        request, "rooms/search.html", {"city": city}
    )  # html 이용가능하게 city를 context에 넣어주고
