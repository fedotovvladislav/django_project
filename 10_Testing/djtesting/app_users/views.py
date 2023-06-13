from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import DetailView

from app_users.models import Order


class OrderDetailView(PermissionRequiredMixin, DetailView):
    permission_required = 'app_users.view_order'
    template_name = 'app_users/order_detail.html'
    model = Order
    context_object_name = 'order'


class OrderExportView(UserPassesTestMixin, View):

    def test_func(self):
        return self.request.user.is_staff

    def get(self, request: HttpRequest) -> JsonResponse:
        orders = Order.objects.prefetch_related('products').select_related('user').all()
        orders_data = [
            {
                'delivery_address': order.delivery_address,
                'promocode': order.promocode,
                'user': order.user.id,
                'products': [
                    [
                        product.id,
                        product.name
                    ]
                    for product in order.products.all()
                ]
            }
            for order in orders
        ]
        return JsonResponse({'orders': orders_data})


