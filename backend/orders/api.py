from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import AccessToken, TokenError
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
import json

class CartView(APIView):
    permission_classes = [AllowAny]

    def get_user_from_token(self, request):
        """
        Validate user using access_token from cookies.
        """
        access_token = request.COOKIES.get('access_token')

        if not access_token:
            raise AuthenticationFailed('توکن دسترسی یافت نشد')

        try:
            access_token_obj = AccessToken(access_token)
            user_id = access_token_obj.payload.get('user_id')
            return user_id
        except TokenError:
            raise AuthenticationFailed('توکن نامعتبر است یا منقضی شده است')

    def get_cart_from_cookie(self, request):
        """
        Retrieve cart data from cookies for unauthenticated users.
        """
        cart_data = request.COOKIES.get('cart')
        return json.loads(cart_data) if cart_data else {'items': []}

    def get(self, request):
        """
        Get the cart for the current user or from cookies if unauthenticated.
        """
        try:
            user_id = self.get_user_from_token(request)
            # Logged-in user: Retrieve or create a cart in the database
            cart, _ = Cart.objects.get_or_create(customer_id=user_id, is_active=True)
            serializer = CartSerializer(cart)
            return Response(serializer.data)
        except AuthenticationFailed:
            # Anonymous user: Retrieve cart from cookies
            cart_data = self.get_cart_from_cookie(request)
            return Response({'id': None, 'customer': None, 'items': cart_data['items']})

    def post(self, request):
        """
        Add or update cart item for the current user or in cookies if unauthenticated.
        """
        try:
            user_id = self.get_user_from_token(request)
            # Logged-in user: Add or update cart item in the database
            cart, _ = Cart.objects.get_or_create(customer_id=user_id, is_active=True)
            data = request.data
            item, created = CartItem.objects.update_or_create(
                cart=cart,
                product_id=data['product'],
                defaults={
                    'product_name': data['product_name'],
                    'product_price': data['product_price'],
                    'quantity': data['quantity']
                }
            )
            cart.total_price = sum(item.price for item in cart.items.all())
            cart.save()
            serializer = CartSerializer(cart)
            return Response(serializer.data)
        except AuthenticationFailed:
            # Anonymous user: Add or update cart item in cookies
            cart_data = self.get_cart_from_cookie(request)
            items = cart_data['items']
            updated = False
            for item in items:
                if item['product'] == request.data['product']:
                    item['quantity'] += request.data['quantity']
                    updated = True
                    break
            if not updated:
                items.append(request.data)
            cart_data['items'] = items
            response = Response({'message': 'Cart updated in cookie'})
            response.set_cookie('cart', json.dumps(cart_data), httponly=True)
            return response
