from django import forms
from . import models  # 여기서 유저네임 가져올거라서


class LoginForm(forms.Form):
    # django 는 로그인형태로 아이디 이메일 암호를 요구한다
    # 근데 여기서 아이디랑 이메일을 같은걸로 만들거야 한번에 처리하게

    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    # passwordInput 쓰는게 아니라 charField쓰고 형태를 암호에 맞게 바꿀거야(widget이용)

    # email이 있는 field를 확인하고 싶으면 method는 무조건 clean_으로 붙여야함 규칙임

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        try:
            user = models.User.objects.get(email=email)
            if user.check_password(password):
                return self.cleaned_data
                # def 로 clean을 썻으면 언제나 cleaned_data를 return 받아야해
            else:
                self.add_error("password", forms.ValidationError("Password is wrong"))
        except models.User.DoesNotExist:
            self.add_error("email", forms.ValidationError("User does not exist"))


class SignUpForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ("first_name", "last_name", "email")

    password = forms.CharField(widget=forms.PasswordInput)
    password1 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    def clean_password1(self):
        password = self.cleaned_data.get("password")
        password1 = self.cleaned_data.get("password1")
        if password != password1:
            raise forms.ValidationError("Password confirmation does not match")
        else:
            return password

    def save(self, *args, **kwargs):
        user = super().save(commit=False)
        # commit=False -> object를 생성하지만 데이터베이스로 보내지는 말라는 것
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        user.username = email
        user.set_password(password)
        user.save()
