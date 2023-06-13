from django.core.management import BaseCommand

from app_users.models import Product


class Command(BaseCommand):
    def handle(self, *args, **options):
        products_list = [
            {
                "name": 'Laptop',
                "description": "Best Laptop",
                "price": 10000,
                "discount": 10,
            },
            {
                "name": 'Smartphone',
                "description": "Best Smartphone",
                "price": 20000,
                "discount": 15,
            },
            {
                "name": 'TV',
                "description": "Best TV",
                "price": 30000,
                "discount": 30,
            },
        ]
        for product in products_list:
            product = Product.objects.create(
                name=product['name'],
                description=product['description'],
                price=product['price'],
                discount=product['discount']
            )