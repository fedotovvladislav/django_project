from django import forms
from . import models


class NewsForm(forms.ModelForm):

    class Meta:
        model = models.NewsModel
        fields = ['name', 'description']


class CommentsForm(forms.ModelForm):

    class Meta:
        model = models.CommentsModel
        fields = ['user_name', 'comment']
