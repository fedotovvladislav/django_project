from django.urls import path
from . import views

urlpatterns = [
    path('start_page/', views.start_page, name='start_page'),
    path('python_basic/', views.python_basic, name='python_basic'),
    path('java/', views.java, name='java'),
    path('motion/', views.motion, name='motion'),
    path('web_layout/', views.web_layout, name='web_layout'),
    path('django_frame/', views.django_frame, name='django_frame')
]
