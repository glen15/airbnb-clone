from math import ceil
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage
from . import models


def all_rooms(request):
    page = request.GET.get("page", 1)
    room_list = (
        models.Room.objects.all()
    )  # 쿼리셋만 만들뿐 즉시 불러오는건 아니다 = 데이터베이스에 all이 다들어가는 사태는 안일어나
    paginator = Paginator(
        room_list, 10, orphans=5
    )  # orphans 남는애들인데 이렇게 5로 지정하면 5개까지는 마지막페이지에 넣어서 보여줌

    try:
        rooms = paginator.page(int(page))  # 11.3 commit에 수동으로한걸 자동으로 해줌
        return render(request, "rooms/home.html", {"page": rooms})
    except EmptyPage:
        return redirect("/")  # 홈으로 리다이렉트 시켜서 유저가 url을 막써놓은걸 다시 정리 시켜주는 것
