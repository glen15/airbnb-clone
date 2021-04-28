# 이게 통과해야 다음으로 넘어가게하는거지
# 로그인 상황인데, url에 로그인url 넣어서 그 창으로 못가게할거야
# 로그라이크 같은거에서 url만 고쳐서 들어가는걸 막을 수도 ?

from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin


class LoggedOutOulyView(UserPassesTestMixin):

    permission_denied_message = "Page not found"

    def test_func(self):
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        messages.error(self.request, "Can't go there")
        return redirect("core:home")
        # 로그인되어있는데 로그인페이지로 강제로 url넣고 이동하려고하면 그냥 홈으로 보내버리는거야


# 로그인 안한상태에서 edit profile 가는걸 막는거지
class loggedInOnlyView(LoginRequiredMixin):
    login_url = reverse_lazy("users:login")


# 카톡로그인했는데 비밀번호바꾸러가는 놈들 못가게
class EmailLoginOnlyView(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.login_method == "email"

    def handle_no_permission(self):
        messages.error(self.request, "Can't go there")
        return redirect("core:home")
