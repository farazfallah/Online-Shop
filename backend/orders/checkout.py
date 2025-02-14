from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from customers.models import Address
from orders.models import Cart, Order, OrderItem, DiscountCode
from orders.serializers import OrderSerializer, CartItemSerializer, AddressSerializer
from core.utils import get_user_from_token
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
            return Response({'error': 'سبد خرید خالی است'}, status=400)

        address_id = request.data.get('address_id')
        if not address_id:
            return Response({'error': 'آدرس تحویل الزامی است'}, status=400)

        try:
            shipping_address = Address.objects.get(id=address_id, customer_id=user_id)
        except Address.DoesNotExist:
            return Response({'error': 'آدرس انتخاب شده معتبر نیست'}, status=400)

        total_price = Decimal('0')
        order_items = []

        for cart_item in cart.items.select_related('product').all():
            product = cart_item.product
            
            if product.stock_quantity < cart_item.quantity:
                return Response({
                    'error': f'محصول {product.name} به تعداد درخواستی موجود نیست'
                }, status=400)
            
            current_price = product.price - (product.price * Decimal(product.discount) / 100)
            
            order_items.append({
                'product': product,
                'quantity': cart_item.quantity,
                'product_price': current_price,
            })
            
            total_price += current_price * cart_item.quantity

        discount_code = request.data.get('discount_code')
        applied_discount = None
        
        if discount_code:
            try:
                discount = DiscountCode.objects.get(
                    code=discount_code,
                    is_active=True
                )
                total_price = total_price - (total_price * discount.discount_percentage / 100)
                applied_discount = discount
            except DiscountCode.DoesNotExist:
                return Response({'error': 'کد تخفیف نامعتبر است'}, status=400)

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

        response_data = {
            'order': OrderSerializer(order, context={'request': request}).data,
            'message': 'سفارش با موفقیت ثبت شد'
        }

        if applied_discount:
            response_data['applied_discount'] = {
                'code': applied_discount.code,
                'percentage': float(applied_discount.discount_percentage)
            }

        return Response(response_data, status=201)

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

        cart_items = CartItemSerializer(
            cart.items.select_related('product').all(), 
            many=True,
            context={'request': request}
        ).data

        total_price = Decimal('0')
        for cart_item in cart.items.all():
            product = cart_item.product
            current_price = product.price - (product.price * Decimal(product.discount) / 100)
            total_price += current_price * cart_item.quantity

        response_data = {
            'items': cart_items,
            'total_price': float(total_price),
            'items_count': cart.items.count(),
        }

        return Response(response_data)