from django.urls import path
from . import views

urlpatterns = [
    path('create_news/', views.CreateNews.as_view(), name='create_news'),
    path('all_news/', views.NewsListView.as_view(), name='all_news'),
    path('all_news/<int:pk>', views.NewsDetailView.as_view(), name='detail_view'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout')
]
