from django.urls import path
from .views import ListArticlesView

app_name = 'blogapp'

urlpatterns = [
    path('articles/', ListArticlesView.as_view(), name='list_articles'),
]