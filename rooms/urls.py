from django.urls import path
from . import views

app_name = "rooms"

urlpatterns = [
    path("<int:pk>", views.room_detail, name="detail")
]  # 각 룸 id를 url뒤에 붙여서 링크연결되도록
