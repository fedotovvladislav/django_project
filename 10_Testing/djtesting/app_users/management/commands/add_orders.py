from django.contrib.auth.models import User
from django.core.management import BaseCommand

from app_users.models import Order, Product


class Command(BaseCommand):
    def handle(self, *args, **options):
        orders_list = [
            {
                "delivery_address": "Moscow,  70 years of victory, 15-24",
                "promocode": "123415ga",
                "user": User.objects.get(pk=1),
            },
            {
                "delivery_address": "Spb,  Gorokhovaya Street, 17-31",
                "promocode": "5123456asd",
                "user": User.objects.get(pk=1),
            },
        ]
        products = Product.objects.all()
        for order in orders_list:
            order = Order.objects.create(
                delivery_address=order["delivery_address"],
                promocode=order["promocode"],
                user=order["user"],
            )
            for product in products:
                order.products.add(product)
