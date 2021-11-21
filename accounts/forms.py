from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from django.shortcuts import redirect

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'image',)
        # fields = UserCreationForm.Meta.fields

class CustomUserChangeForm(UserChangeForm):
    password = None # password 필드 관련 정보 숨기기

    class Meta:
        model = get_user_model()
        fields = ('username', 'image',)

# class KakaoSignInView(View):
#     def get(self, request):
#         app_key = '42a0571fe9d27ca9810a5e953a9f87fc'
#         redirect_uri = 'http://localhost:8000/accounts/kakao/login/callback/'
#         kakao_auth_api = 'https://kauth.kakao.com/oauth/authorize?response_type=code'
#         return redirect (f'{kakao_auth_api}&client_id={app_key}&redirect_uri={redirect_uri}')