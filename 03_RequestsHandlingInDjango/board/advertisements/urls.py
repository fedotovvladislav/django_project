from django.urls import path
from . import views

urlpatterns = [
    path('advertisement/', views.Advertisement.as_view(), name='advertisement'),
    path('contacts/', views.Contacts.as_view()),
    path('about/', views.AboutUs.as_view()),
    path('', views.HomePage.as_view())
]
