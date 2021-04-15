from django.views import View
from django.shortcuts import render  # render 할때 import 할것


class LoginView(View):
    def get(self, request):
        return render(request, "users/login.html")

    def post(self, request):
        pass