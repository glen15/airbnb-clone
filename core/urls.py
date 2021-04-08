from django.urls import path
from rooms import views as room_views

app_name = "core"  # config에 있는 urls.py에 있는 urlpatterns의 spacename 과 일치해야한다

# urlpatterns 변수명은 필수, 옵션이 아님
urlpatterns = [path("", room_views.all_rooms, name="home")]
# rooms 어플폴더에서 views.py 파일을 room_views라는 이름으로 import 해놓은 경로로 가져와서 그안 에 있는 all_rooms 함수를 실행시킨것
