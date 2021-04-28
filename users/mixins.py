# 이게 통과해야 다음으로 넘어가게하는거지
# 로그인 상황인데, url에 로그인url 넣어서 그 창으로 못가게할거야
# 로그라이크 같은거에서 url만 고쳐서 들어가는걸 막을 수도 ?

from django.shortcuts import redirect
from django.contrib.auth.mixins import UserPassesTestMixin


class LoggedOulyView(UserPassesTestMixin):

    permission_denied_message = "Page not found"

    def test_func(self):
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        return redirect("core:home")
        # 로그인되어있는데 로그인페이지로 강제로 url넣고 이동하려고하면 그냥 홈으로 보내버리는거야
