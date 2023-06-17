from .models import Product, Order
from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            'name',
            'description',
            'price',
            'discount',
            'archived',
        ]


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            "id",
            'delivery_address',
            'promocode',
            'user',
            'products',
        ]

    def to_representation(self, instance):
        rep = super(OrderSerializer, self).to_representation(instance)
        rep['products'] = [
            {
                "id": product.id,
                "name": product.name
            }
            for product in instance.products.all()]
        rep['user'] = {
            "id": instance.user.id,
            "username": instance.user.username
        }
        return rep