from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model


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