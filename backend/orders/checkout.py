from django.shortcuts import get_object_or_404
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from orders.models import Cart, Order, OrderItem, DiscountCode
from orders.serializers import OrderSerializer, AddressSerializer
from core.utils import get_user_from_token
from product.models import Product
from decimal import Decimal


class CheckoutView(APIView):
    @transaction.atomic
    def post(self, request):
        try:
            user_id = get_user_from_token(request)
        except AuthenticationFailed as e:
            return Response({'error': str(e)}, status=401)

        cart = Cart.objects.filter(
            customer_id=user_id,
            is_active=True
        ).first()

        if not cart or not cart.items.exists():
            raise ValidationError({'error': 'سبد خرید خالی است'})

        address_data = request.data.get('shipping_address')
        if not address_data:
            raise ValidationError({'error': 'آدرس تحویل الزامی است'})

        address_serializer = AddressSerializer(data=address_data)
        if not address_serializer.is_valid():
            raise ValidationError(address_serializer.errors)
        
        shipping_address = address_serializer.save(customer_id=user_id)

        total_price = Decimal('0')
        order_items = []

        for cart_item in cart.items.all():
            product = get_object_or_404(Product, id=cart_item.product.id)
            
            if product.stock_quantity < cart_item.quantity:
                raise ValidationError({
                    'error': f'محصول {product.name} به تعداد درخواستی موجود نیست'
                })
            
            current_price = product.price - (product.price * Decimal(product.discount) / 100)
            
            order_items.append({
                'product': product,
                'quantity': cart_item.quantity,
                'product_price': current_price
            })
            
            total_price += current_price * cart_item.quantity

        discount_code = request.data.get('discount_code')
        if discount_code:
            try:
                discount = DiscountCode.objects.get(
                    code=discount_code,
                    is_active=True
                )
                total_price = total_price - (total_price * discount.discount_percentage / 100)
            except DiscountCode.DoesNotExist:
                raise ValidationError({'error': 'کد تخفیف نامعتبر است'})

        order = Order.objects.create(
            customer_id=user_id,
            shipping_address=shipping_address,
            total_price=total_price,
            status='registered'
        )

        for item in order_items:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                product_name=item['product'].name,
                product_price=item['product_price'],
                quantity=item['quantity'],
                price=item['product_price'] * item['quantity']
            )
            
            product = item['product']
            product.stock_quantity -= item['quantity']
            product.save()

        cart.is_active = False
        cart.save()

        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def get(self, request):
        try:
            user_id = get_user_from_token(request)
        except AuthenticationFailed as e:
            return Response({'error': str(e)}, status=401)

        cart = Cart.objects.filter(
            customer_id=user_id,
            is_active=True
        ).first()

        if not cart or not cart.items.exists():
            raise ValidationError({'error': 'سبد خرید خالی است'})

        total_price = Decimal('0')
        items_summary = []

        for cart_item in cart.items.all():
            product = get_object_or_404(Product, id=cart_item.product.id)
            current_price = product.price - (product.price * Decimal(product.discount) / 100)
            
            items_summary.append({
                'product_name': product.name,
                'quantity': cart_item.quantity,
                'price': current_price * cart_item.quantity
            })
            
            total_price += current_price * cart_item.quantity

        return Response({
            'items': items_summary,
            'total_price': total_price
        })