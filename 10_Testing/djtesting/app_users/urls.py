from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.urls import path

from app_users.views import OrderDetailView, OrderExportView

app_name = 'app_users'

urlpatterns = [
    path('order/detail/<int:pk>', OrderDetailView.as_view(), name='order_detail'),
    path('login/', LoginView.as_view(template_name='app_users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('orders/export/', OrderExportView.as_view(), name='orders_export'),
]