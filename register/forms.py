from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm, UserCreationForm, PasswordChangeForm,
    PasswordResetForm, SetPasswordForm
)
from django.contrib.auth import get_user_model
from .models import Shops,UserData
User = get_user_model()


class EmailChangeForm(forms.ModelForm):
    """メールアドレス変更フォーム"""

    class Meta:
        model = User
        fields = ('email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def clean_email(self):
        email = self.cleaned_data['email']
        User.objects.filter(email=email, is_active=False).delete()
        if User.objects.filter(email=email).count() != 0:
            raise forms.ValidationError(
            "このメールアドレスは既に登録されています。"
            )
        return email


class LoginForm(AuthenticationForm):
    """ログインフォーム"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label  # placeholderにフィールドのラベルを入れる



class UserCreateForm(UserCreationForm):
    """ユーザー登録用フォーム"""

    class Meta:
        model = User
        fields = ('email', 'last_name','first_name',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label
    def clean_email(self):
        email = self.cleaned_data['email']
        User.objects.filter(email=email, is_active=False).delete()
        return email        

class ShopsForm(forms.ModelForm):
    class Meta:
        model = Shops
        fields = ("shop",
        )
        
class UserDataForm(forms.ModelForm):
    class Meta:
        model = UserData
        fields =("date_of_birth","start_day",
        )        
        widgets = {
            'date_of_birth': forms.SelectDateWidget(years=[x for x in range(1970, 2005)]),
            'start_day': forms.SelectDateWidget(years=[x for x in range(2020, 2020)]),
        }

#
#
# class UserUpdateForm(forms.ModelForm):
#     """ユーザー情報更新フォーム"""
#
#     class Meta:
#         model = User
#         fields = ('first_name', 'last_name',)
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for field in self.fields.values():
#             field.widget.attrs['class'] = 'form-control'
#
#
# class MyPasswordChangeForm(PasswordChangeForm):
#     """パスワード変更フォーム"""
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for field in self.fields.values():
#             field.widget.attrs['class'] = 'form-control'
#
#
# class MyPasswordResetForm(PasswordResetForm):
#     """パスワード忘れたときのフォーム"""
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for field in self.fields.values():
#             field.widget.attrs['class'] = 'form-control'
#
#
# class MySetPasswordForm(SetPasswordForm):
#     """パスワード再設定用フォーム(パスワード忘れて再設定)"""
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for field in self.fields.values():
#             field.widget.attrs['class'] = 'form-control'
