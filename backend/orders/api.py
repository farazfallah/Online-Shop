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
