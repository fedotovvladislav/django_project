from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.Register.as_view(), name='register'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/<int:pk>', views.ProfileDetailView.as_view(), name='profile_detail'),
    path('all_news/', views.NewsListView.as_view(), name='all_news'),
    path('all_news/<int:pk>', views.NewsDetailView.as_view(), name='detail_view'),
    path('all_news/<slug>', views.NewsListView.as_view(), name='all_news_by_tag'),
    path('create_news/', views.CreateNews.as_view(), name='create_news'),
]