from rest_framework.serializers import ModelSerializer
from rest_framework.relations import HyperlinkedIdentityField
from django.core import serializers

from .models import Product, Order


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "pk",
            "name",
            "description",
            "price",
            "discount",
            "created_at",
            "archived",
            "preview",
        )


class OrderSerializer(ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = (
            "pk",
            "user",
            "products",
            "created_at",
            "promocode",
            "delivery_address",
        )


