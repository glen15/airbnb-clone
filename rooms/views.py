from django.views.generic import ListView, DetailView, UpdateView, View
from django.shortcuts import render
from django.core.paginator import Paginator
from . import models, forms

# 밑에 둘은 function기반으로할때 사용
# from django.http import Http404
# from django.shortcuts import render, redirect
# from django.urls import reverse


class HomeView(ListView):  # core폴더의 url에도 넣어뒀음

    """ HomeView Definition """

    model = models.Room
    paginate_by = 12  # ListView 관련사항 ccv.co.uk확인하면 잘 정리되어있음
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


class SearchView(View):

    """ Search View Definition"""

    def get(self, request):
        country = request.GET.get("country")
        if country:
            form = forms.SearchForm(
                request.GET
            )  # request.GET 넣어서 서치버튼 눌렀을때 설정 기억하도록하는 것
            if form.is_valid():  # if 오류가 없다면
                city = form.cleaned_data.get("city")
                country = form.cleaned_data.get("country")
                room_type = form.cleaned_data.get("room_type")
                price = form.cleaned_data.get("price")
                guests = form.cleaned_data.get("guests")
                bedrooms = form.cleaned_data.get("bedrooms")
                beds = form.cleaned_data.get("beds")
                baths = form.cleaned_data.get("baths")
                instant_book = form.cleaned_data.get("instant_book")
                superhost = form.cleaned_data.get("superhost")
                amenities = form.cleaned_data.get("amenities")
                facilities = form.cleaned_data.get("facilities")

                filter_args = {}

                if city != "Anywhere":
                    filter_args["city__startswith"] = city

                filter_args["country"] = country

                if room_type is not None:
                    filter_args["room_type"] = room_type

                if price is not None:
                    filter_args["price__lte"] = price  # lte 작거나 같음

                if guests is not None:
                    filter_args["guests__gte"] = guests  # gte 크거나 같음

                if bedrooms is not None:
                    filter_args["bedrooms__gte"] = bedrooms

                if beds is not None:
                    filter_args["beds__gte"] = beds

                if baths is not None:
                    filter_args["baths__gte"] = baths

                if instant_book is True:
                    filter_args["instant_book"] = True  # moelds.py에 있는 instant_book 이름

                if superhost is True:
                    filter_args["host__superhost"] = True

                for amenity in amenities:
                    filter_args["amenities"] = amenity

                for facility in facilities:
                    filter_args["facilities"] = facility

                qs = models.Room.objects.filter(**filter_args).order_by("-created")

                paginator = Paginator(qs, 10, orphans=5)

                page = request.GET.get("page", 1)

                rooms = paginator.get_page(page)

                return render(
                    request, "rooms/search.html", {"form": form, "rooms": rooms}
                )

        else:
            form = forms.SearchForm()
            # 첫form을 가져와야할때(데이터확인과정없는 순간)  request.GET아닌걸로 연결해서 required 안뜨게 하는거
        return render(request, "rooms/search.html", {"form": form})


class EditRoomView(UpdateView):
    model = models.Room
    template_name = "rooms/room_edit.html"
    fields = (
        "name",
        "description",
        "price",
        "address",
        "guests",
        "beds",
        "baths",
        "check_in",
        "check_out",
        "room_type",
        "amenities",
        "facilities",
        "house_rules",
    )