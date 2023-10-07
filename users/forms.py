from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from users.models import User


class UserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("email", "password1", "password2")


class UserProfileForm(UserChangeForm):

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "password")

    # def __init__(self, *args, **kwargs):
    #     super(UserChangeForm, self).__init__(self, *args, **kwargs)
    #     self.fields['password'].widget = forms.HiddenInput()

    password = forms.CharField(label='reset', max_length=256, widget=forms.HiddenInput())


class VerificationForm(UserChangeForm):

    password = forms.CharField(label='reset', max_length=256, widget=forms.HiddenInput(), required=False)

    class Meta:
        model = User
        fields = ("is_verified",)

