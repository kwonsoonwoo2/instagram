from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import User

# 1. 사용자 모델 클래스에 대한 참조가 필요할때
# get_user_model() 함수를 사용
#   -> settings.AUTH_USER_MODEL
User = get_user_model()

class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._user = None

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    def clean(self):
        super().clean()
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError('사용자명 또는 비밀번호가 올바르지 않다')
        self._user = user

    @property
    def user(self):
        if self.errors:
            raise ValueError('폼의 데이터 유효성 검증에 실패하였다')
        return self._user


class SignupForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    def clean_username(self):
        data = self.cleaned_data['username']
        if User.objects.filter(username=data).exists():
            raise forms.ValidationError('이미 사용중인 유저네임 입니다.')
        return data

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 != password2:
            raise forms.ValidationError('비밀번호랑 비밀번호 확인값이 안맞음요.')
        return password2

    def save(self):
        if self.errors:
            raise ValueError('폼의 데이터 유효성 검증에 실패함')
        user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['password2'],
        )
        return user
