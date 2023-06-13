from django.contrib.auth.models import User, Permission
from django.test import TestCase
from django.urls import reverse

from app_users.models import Order, Product


class OrderDetailViewTestCase(TestCase):
    fixture = [
        "products_list.json"
    ]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(
            username='Antony',
            password='123qwe'
        )
        permission = Permission.objects.get(
            codename='view_order'
        )
        cls.user.user_permissions.add(permission)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self):
        self.order = Order.objects.create(
            delivery_address="NN,  Permyakova Street, 25-17",
            promocode="5123456asd",
            user=self.user,
        )
        products = Product.objects.all()
        for product in products:
            self.order.products.add(product)

        self.client.force_login(self.user)

    def tearDown(self):
        self.order.delete()

    def test_order_detail_view(self):
        response = self.client.get(
            reverse("app_users:order_detail", kwargs={"pk": self.order.pk}),
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Address')
        self.assertContains(response, 'Promocode')
        self.assertEqual(response.context['order'], self.order)


class OrdersExportTestCase(TestCase):
    fixtures = [
        "orders_list.json",
        "products_list.json",
        "users_list.json",
    ]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(
            username='Antony',
            password='123qwe',
            is_staff=True,
        )

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self) -> None:
        self.client.force_login(self.user)

    def test_export_orders(self):
        response = self.client.get(
            reverse("app_users:orders_export")
        )
        self.assertEqual(response.status_code, 200)
        orders = Order.objects.prefetch_related("products").select_related("user").all()
        expected_data = [
            {
                'delivery_address': order.delivery_address,
                'promocode': order.promocode,
                'user': order.user.id,
                'products': [
                    [
                        product.id, product.name
                    ] for product in order.products.all()
                ]
            }
            for order in orders
        ]
        orders_data = response.json()
        self.assertEqual(
            expected_data,
            orders_data['orders']
        )


