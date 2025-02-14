from decimal import Decimal
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from orders.models import Cart, DiscountCode, Order
from orders.serializers import OrderSerializer
from core.utils import get_user_from_token


class OrderListView(APIView):
    
    def get(self, request, *args, **kwargs):
        user_id = get_user_from_token(request)
        orders = Order.objects.filter(customer_id=user_id)
        serializer = OrderSerializer(orders, many=True, context={'request': request})
        return Response(serializer.data, status=200)
    

class OrderDetailView(APIView):
    
    def get(self, request, order_id, *args, **kwargs):
        user_id = get_user_from_token(request)
        
        try:
            order = Order.objects.get(id=order_id, customer_id=user_id)
            serializer = OrderSerializer(order, context={'request': request})
            return Response(serializer.data, status=200)
            
        except Order.DoesNotExist:
            return Response(
                {'error': 'Order not found'}, 
                status=404
            )


class VerifyDiscountView(APIView):
    def post(self, request):
        try:
            user_id = get_user_from_token(request)
        except AuthenticationFailed as e:
            return Response({'error': str(e)}, status=401)
            
        discount_code = request.data.get('discount_code')
        if not discount_code:
            return Response({
                'valid': False,
                'message': 'کد تخفیف الزامی است'
            }, status=400)

        try:
            discount = DiscountCode.objects.get(
                code=discount_code,
                is_active=True
            )
            
            # دریافت سبد خرید فعال
            cart = Cart.objects.filter(
                customer_id=user_id,
                is_active=True
            ).first()
            
            if not cart or not cart.items.exists():
                return Response({
                    'valid': False,
                    'message': 'سبد خرید خالی است'
                }, status=400)
                
            # محاسبه قیمت کل
            total_price = Decimal('0')
            for cart_item in cart.items.all():
                product = cart_item.product
                current_price = product.price - (product.price * Decimal(product.discount) / 100)
                total_price += current_price * cart_item.quantity
                
            # محاسبه قیمت با اعمال کد تخفیف
            new_total = total_price - (total_price * discount.discount_percentage / 100)
            
            return Response({
                'valid': True,
                'percentage': float(discount.discount_percentage),
                'new_total': float(new_total)
            })
            
        except DiscountCode.DoesNotExist:
            return Response({
                'valid': False,
                'message': 'کد تخفیف نامعتبر است'
            }, status=400)