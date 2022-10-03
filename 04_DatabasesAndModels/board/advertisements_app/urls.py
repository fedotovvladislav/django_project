from django.urls import path
from . import views

urlpatterns = [
    path('advertisement/', views.AdvertisementList.as_view(), name='advertisement'),
    path('advertisement/<int:pk>', views.AdvertisementDetail.as_view(), name='advertisement-detail')
]
