from django.views.generic import ListView, DetailView
from django.shortcuts import render
from django_countries import countries
from . import models

# 밑에 둘은 function기반으로할때 사용
# from django.http import Http404
# from django.shortcuts import render, redirect
# from django.urls import reverse


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
    city = request.GET.get("city", "Anywhere")
    # Anywhere은 디폴트값을 줘서, 아무것도 없을때 오류나는 것을 방지
    city = str.capitalize(city)  # 데이터베이스 안에는 첫번째가 대문자로 되어있어서 거기에 맞게 변경
    country = request.GET.get("country", "KR")
    room_type = int(request.GET.get("room_type", 0))
    price = int(request.GET.get("price", 0))
    guests = int(request.GET.get("guests", 0))
    bedrooms = int(request.GET.get("bedrooms", 0))
    beds = int(request.GET.get("beds", 0))
    baths = int(request.GET.get("baths", 0))
    instant = bool(
        request.GET.get("instant", False)
    )  # True가 텍스트로 되어있을 수 있어서 불리언 타입으로 확실하게
    superhost = bool(request.GET.get("superhost", False))
    s_amenities = request.GET.getlist("amenities")
    s_facilities = request.GET.getlist("facilities")
    # 마지막둘은 리스트형식으로 불러와야 체크박스 된 애들을 전부 가져옴

    # request로 받은 것 -> 서치버튼올  찾고 나서도 그페이지에서는 폼을 기억하게
    form = {
        "city": city,
        "s_country": country,
        "s_room_type": room_type,
        "price": price,
        "guests": guests,
        "bedrooms": bedrooms,
        "beds": beds,
        "baths": baths,
        "instant": instant,
        "superhost": superhost,
        "s_amenities": s_amenities,
        "s_facilities": s_facilities,
    }

    room_types = models.RoomType.objects.all()
    amenities = models.Amenity.objects.all()
    facilities = models.Facility.objects.all()

    # 데이터베이스에서 받은것 -> 목록보여주기용
    choices = {
        "countries": countries,
        "room_types": room_types,
        "amenities": amenities,
        "facilities": facilities,
    }

    filter_args = {}

    if city != "Anywhere":
        filter_args["city__startswith"] = city

    filter_args["country"] = country

    if room_type != 0:
        filter_args["room_type__pk"] = room_type
        # room_type은 forignkey이고 거기서 __pk로 그안에서 pk를 필터링해서 가져오는 것

    if price != 0:
        filter_args["price__lte"] = price  # lte 작거나 같음

    if guests != 0:
        filter_args["guests__gte"] = guests  # gte 크거나 같음

    if bedrooms != 0:
        filter_args["bedrooms__gte"] = bedrooms

    if beds != 0:
        filter_args["beds__gte"] = beds

    if baths != 0:
        filter_args["baths__gte"] = baths

    if instant is True:
        filter_args["instant_book"] = True  # moelds.py에 있는 instant_book 이름

    if superhost is True:
        filter_args["host__superhost"] = True

    if len(s_amenities) > 0:
        for s_amenity in s_amenities:
            filter_args["amenities__pk"] = int(s_amenity)

    if len(s_facilities) > 0:
        for s_facility in s_facilities:
            filter_args["facilities__pk"] = int(s_facility)

    rooms = models.Room.objects.filter(**filter_args)

    return render(
        request,
        "rooms/search.html",
        {**form, **choices, "rooms": rooms},
    )
    # html 이용가능하게 city를 context에 넣어주고
    # from 이랑 choices가 딕셔너리 구조라서 +가 안되서 ** 이용해서 다 언팩해둔것
