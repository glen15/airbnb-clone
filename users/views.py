import os
import requests  # pipenv install requests 해서 설치하고 가져온 것
from django.utils import translation
from django.http import HttpResponse
from django.contrib.auth.views import PasswordChangeView
from django.views import View
from django.views.generic import FormView, DetailView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile  # raw content를 만들어서 사진넣으려고 하는거
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from . import forms, models, mixins


class LoginView(mixins.LoggedOutOulyView, FormView):

    template_name = "users/login.html"
    form_class = forms.LoginForm

    # success_url = reverse_lazy("core:home")
    # 뒤에 get_success_url 사용으로 변경 -> 기존에 가려던 화면 유지해주기 위해서, - 프로필 에디트 하려했는데 로그인하라고해서 로그인하면 원래 하려던 프로필 에디터러 가도록
    # reverse 는 뒤에있는 애로 가서 그 친구의 실제 url을 가져온다
    # reverse_lazy는 바로 안불러오고 view를 불러올 때 부른다

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        user.verify_email()
        return super().form_valid(form)

    def get_success_url(self):
        next_arg = self.request.GET.get("next")  # url 쿼리에서 next인자값을 받아오는거지
        if next_arg is not None:
            return next_arg
        else:
            return reverse("core:home")


def log_out(request):
    messages.info(request, f"See you later {request.user.first_name}")
    logout(request)
    return redirect(reverse("core:home"))


class SignUpView(FormView):
    template_name = "users/signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        user.verify_email()
        return super().form_valid(form)


def complete_verification(request, key):
    try:
        user = models.User.objects.get(email_secret=key)
        user.email_verified = True
        user.email_secret = ""  # 인증 후 지우는 것
        user.save()
        # to do : add succes message    dajango message framework를 참고할것
    except models.User.DoesNotExist:
        # to do : add error message
        pass
    return redirect(reverse("core:home"))


def github_login(request):
    client_id = os.environ.get("GH_ID")
    redirect_uri = "http://127.0.0.1:8000/users/login/github/callback"
    return redirect(
        f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope=read:user"
    )


class GithubException(Exception):
    pass


def github_callback(request):
    try:
        client_id = os.environ.get("GH_ID")
        client_secret = os.environ.get("GH_SECRET")
        code = request.GET.get("code", None)
        if code is not None:
            # requetsts를 받아서 토큰이랑 교환하도록 보내는 것
            # https://docs.github.com/en/developers/apps/authorizing-oauth-apps 참고
            token_request = requests.post(
                f"https://github.com/login/oauth/access_token?client_id={client_id}&client_secret={client_secret}&code={code}",
                headers={"Accept": "application/json"},
            )
            token_json = token_request.json()
            error = token_json.get("error", None)
            if error is not None:
                raise GithubException("Can't get acess token")
            else:
                access_token = token_json.get("access_token")
                profile_request = requests.get(
                    "https://api.github.com/user",
                    headers={
                        "Authorization": f"token {access_token}",
                        "Accept": "application/json",
                    },
                )
                profile_json = profile_request.json()
                username = profile_json.get("login", None)
                if username is not None:
                    name = profile_json.get("name")
                    name = username if name is None else name  # github에 네임없는 계정의 경우
                    email = profile_json.get("email")
                    email = name + "@email.com" if email is None else email
                    bio = profile_json.get("bio")
                    bio = "" if bio is None else bio  # guthub에 바이오 없는 계정의 경우
                    try:
                        user = models.User.objects.get(email=email)
                        if (
                            user.login_method != models.User.LOGIN_GITHUB
                        ):  # 깃헙 외의 방법으로 로그인하려했던거지,카카오나
                            raise GithubException(
                                f"Please log in with {user.login_method}"
                            )
                    except models.User.DoesNotExist:  # 유저가 존재하지 않는 경우 = 새로 생성해야하는 경우지
                        user = models.User.objects.create(
                            email=email,
                            first_name=name,
                            username=email,
                            bio=bio,
                            login_method=models.User.LOGIN_GITHUB,
                            email_verified=True,
                        )
                        user.set_unusable_password()
                        user.save()
                    login(request, user)
                    messages.success(request, f"Welcome back {user.first_name}")
                    return redirect(reverse("core:home"))
                else:
                    raise GithubException("Can't get your profile")
        else:
            raise GithubException("Can't get code")
    except GithubException as e:  # 뭐든 에러가 나면 login으로 보내버리도록
        messages.error(request, e)
        return redirect(reverse("users:login"))


def kakao_login(request):
    client_id = os.environ.get("KAKAO_ID")
    redirect_uri = "http://127.0.0.1:8000/users/login/kakao/callback"
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
    )


class KakaoException(Exception):
    pass


def kakao_callback(request):
    try:
        code = request.GET.get("code")  # 코드를 받았으니 호스트에게 포스트로 보내야지
        client_id = os.environ.get("KAKAO_ID")
        redirect_uri = "http://127.0.0.1:8000/users/login/kakao/callback"
        token_request = requests.get(
            f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={redirect_uri}&code={code}"
        )
        token_json = token_request.json()
        error = token_json.get("error", None)
        if error is not None:  # 에러가 존재한다면
            raise KakaoException("Can't get authorization code.")
        access_token = token_json.get("access_token")
        profile_request = requests.get(
            "https://kapi.kakao.com/v2/user/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        profile_json = profile_request.json()
        # 이 안에 email이나 id nickname profile_image 등등 존재
        kakao_account = profile_json.get("kakao_account", None)
        email = kakao_account.get("email")
        if email is None:
            raise KakaoException("Please also give me your email.")
        properties = profile_json.get("properties")
        nickname = properties.get("nickname")
        profile_image = properties.get("profile_image")
        try:
            user = models.User.objects.get(email=email)
            if user.login_method != models.User.LOGIN_KAKAO:
                raise KakaoException(f"Please log in with: {user.login_method}")
        except models.User.DoesNotExist:
            user = models.User.objects.create(
                email=email,
                username=email,
                first_name=nickname,
                login_method=models.User.LOGIN_KAKAO,
                email_verified=True,
            )
            user.set_unusable_password()
            user.save()
            if profile_image is not None:
                photo_request = requests.get(profile_image)
                user.avatar.save(
                    f"{nickname}-avatar", ContentFile(photo_request.content)
                )
                # content는 0과1로 이루어진 파일을 말함, 텍스트도아니고 json도 아니고
        login(request, user)
        messages.success(request, f"Welcome back {user.first_name}")
        return redirect(reverse("core:home"))
    except KakaoException as e:
        messages.error(request, e)
        return redirect(reverse("users:login"))


class UserProfileView(DetailView):

    model = models.User
    context_object_name = "user_obj"
    # context_object_name 으로 지정안하면 로그인 후 룸디테일 등 에서 다른 유저 프로필을 열었을 때 그게 적용되어버림
    # 이걸 통해서 프로필 눌렀을 때 로그인한 유저의 정보로 연결하도록 해야한다.
    # context 는 기본적으로 랜더해주는 것, 그래서 이게 로그인한 아이디의 프로필로 가도록함


class UpdateProfileView(mixins.loggedInOnlyView, SuccessMessageMixin, UpdateView):

    model = models.User
    template_name = "users/update-profile.html"
    fields = (
        "first_name",
        "last_name",
        "gender",
        "bio",
        "birthdate",
        "language",
        "currency",
    )

    success_message = "Profile updated"

    def get_object(self, queryset=None):
        return self.request.user

    # updateview 에서 plcaeholder사용하는거
    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields["birthdate"].widget.attrs = {"placeholder": "Birthdate"}
        form.fields["first_name"].widget.attrs = {"placeholder": "First name"}
        form.fields["last_name"].widget.attrs = {"placeholder": "Last name"}
        form.fields["bio"].widget.attrs = {"placeholder": "Bio"}

        return form


class UpdatePasswordView(
    mixins.EmailLoginOnlyView,
    mixins.loggedInOnlyView,
    SuccessMessageMixin,
    PasswordChangeView,
):
    template_name = "users/update-password.html"
    success_message = "Password Updated"

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields["old_password"].widget.attrs = {"placeholder": "Current password"}
        form.fields["new_password1"].widget.attrs = {"placeholder": "New password"}
        form.fields["new_password2"].widget.attrs = {
            "placeholder": "New password again"
        }
        return form

    def get_success_url(self):
        return self.request.user.get_absolute_url()


@login_required
def switch_hosting(request):
    try:
        del request.session["is_hosting"]
    except KeyError:
        request.session["is_hosting"] = True
    return redirect(reverse("core:home"))


def switch_language(request):
    lang = request.GET.get("lang", None)
    if lang is not None:
        translation.activate(lang)  #
        response = HttpResponse(200)  #
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang)  #
        # request.session[translation.LANGUAGE_SESSION_KEY] = lang
    return response  # HttpResponse(status=200)
