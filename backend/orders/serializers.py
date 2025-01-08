from rest_framework import serializers
from orders.models import Cart, CartItem

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_name', 'product_price', 'quantity', 'price']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = ['id', 'customer', 'session_id', 'total_price', 'is_active', 'items']
