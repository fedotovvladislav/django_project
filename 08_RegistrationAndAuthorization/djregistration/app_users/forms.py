from django import forms
from django.contrib.auth.forms import UserCreationForm, UsernameField

from . import models


class NewsForm(forms.ModelForm):

    class Meta:
        model = models.NewsModel
        fields = ['name', 'description', 'tags']


class CommentsForm(forms.ModelForm):

    class Meta:
        model = models.CommentsModel
        fields = ['user_name', 'comment']


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = models.User
        fields = ("username",)
        field_classes = {"username": UsernameField}


class ProfileForm(forms.ModelForm):

    class Meta:
        model = models.User
        fields = ['phone', 'city', 'email']
