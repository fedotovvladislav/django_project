from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render
from django.views.generic import DetailView

from app_users.models import Order


class OrderDetailView(PermissionRequiredMixin, DetailView):
    permission_required = 'app_users.view_order'
    template_name = 'app_users/order_detail.html'
    model = Order
    context_object_name = 'order'



