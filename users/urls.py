from django.urls import path
from . import views  # 같은폴더에 있는 views.py 불러오는거지

app_name = "users"  # config urls.py에 넣고나면 app_name 없다고 오류남 그때 이거 작성
urlpatterns = [
    path("login", views.LoginView.as_view(), name="login"),
    path("logout", views.log_out, name="logout"),
    path("signup", views.SignUpView.as_view(), name="signup"),
]
# 위랑 다른 이유: log_out이 import logout에서 가져온 함수이기 때문
#   # urls.py작업해주고 config urls.py 에 추가하기
