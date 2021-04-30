from django.urls import path
from . import views

app_name = "rooms"

urlpatterns = [
    path("<int:pk>/", views.RoomDetail.as_view(), name="detail"),
    path("<int:pk>/edit/", views.EditRoomView.as_view(), name="edit"),
    path("<int:pk>/photos/", views.RoomPhotosView.as_view(), name="photos"),
    path("search/", views.SearchView.as_view(), name="search"),
]
# 각 룸 id를 url뒤에 붙여서 링크연결되도록
# 두번째 인자로 views.room_detail, 넣는게 function 방식으로 reviews만든 것
# views에서 render하고 html 만들고 여기에 path추가
