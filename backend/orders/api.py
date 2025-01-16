from rest_framework.views import APIView
from rest_framework.response import Response
from orders.models import Order
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
