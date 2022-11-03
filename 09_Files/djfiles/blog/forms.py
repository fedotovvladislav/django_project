from django import forms
from django.contrib.auth.forms import UserCreationForm, UsernameField

from . import models


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = models.User
        fields = ("username",)
        field_classes = {"username": UsernameField}


class BlogForm(forms.ModelForm):
    photos = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = models.BlogModel
        fields = ('description', )


class UploadBlogForm(forms.Form):
    file = forms.FileField()