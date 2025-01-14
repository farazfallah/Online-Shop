from rest_framework import serializers
from orders.models import Cart, CartItem, OrderItem, Order, DiscountCode
from customers.serializers import AddressSerializer


class CartItemSerializer(serializers.ModelSerializer):
    product_image = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_name', 'product_price', 'product_image', 'quantity', 'price']

    def get_product_image(self, obj):
        if obj.product_image:
            return obj.product_image
        
        request = self.context.get('request')
        if request and hasattr(obj.product, 'image') and obj.product.image:
            try:
                return request.build_absolute_uri(obj.product.image.url)
            except:
                return None
        
        return None

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = ['id', 'customer', 'session_id', 'total_price', 'is_active', 'items']

class OrderItemSerializer(serializers.ModelSerializer):
    product_image = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'product_price', 'quantity', 'price', 'product_image']
        read_only_fields = ['product_name', 'product_price', 'price', 'product_image']

    def get_product_image(self, obj):
        request = self.context.get('request')
        if request and obj.product.image:
            return request.build_absolute_uri(obj.product.image.url)
        return None

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    shipping_address = AddressSerializer(read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'customer', 'shipping_address', 'total_price', 'status', 'items', 'created_at']
        read_only_fields = ['customer', 'total_price', 'status']

class DiscountCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscountCode
        fields = ['code', 'discount_percentage']
        read_only_fields = ['discount_percentage']