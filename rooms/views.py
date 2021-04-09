from django.shortcuts import render
from . import models
from math import ceil


def all_rooms(request):
    page = request.GET.get("page", 1)
    # request를 통해서 url쪽에서 page 키값의 벨류를 받는데 없으면 1으로하는 것(디폴트)
    page = int(page or 1)  # 페이지가 생성 된 이후에는 위에있는 1을받는 디폴트가 작동안해서 오류페이지가 나오는 것을 방지
    page_size = 10
    limit = page_size * page
    offset = limit - page_size
    all_rooms = models.Room.objects.all()[offset:limit]
    page_count = ceil(models.Room.objects.count() / page_size)
    return render(
        request,
        "rooms/home.html",
        context={
            "rooms": all_rooms,
            "page": page,
            "page_count": page_count,
            "page_range": range(1, page_count),
        },
    )
    # render 통해서 html을 가져오는데, context를 이용해서 여기있는 변수를 html에서 사용할 수 있음.
