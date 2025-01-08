from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import AccessToken, TokenError
from orders.models import Cart, CartItem
from orders.serializers import CartSerializer
from product.models import Product
import json
from decimal import Decimal

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)


class CartView(APIView):
    permission_classes = [AllowAny]

    def get_user_from_token(self, request):
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
        if cart_data:
            cart_data = json.loads(cart_data)
            for item in cart_data['items']:
                item['product_price'] = float(item['product_price'])
                item['price'] = float(item['price'])
            return cart_data
        return {'items': []}


    def get(self, request):
        try:
            user_id = self.get_user_from_token(request)
            cart, _ = Cart.objects.get_or_create(customer_id=user_id, is_active=True)
            serializer = CartSerializer(cart)
            return Response(serializer.data)
        except AuthenticationFailed:
            cart_data = self.get_cart_from_cookie(request)
            return Response({'id': None, 'customer': None, 'items': cart_data['items']})

    def post(self, request):
        try:
            user_id = self.get_user_from_token(request)
            cart, _ = Cart.objects.get_or_create(customer_id=user_id, is_active=True)
            product_id = request.data['product']

            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                return Response({'error': 'محصول یافت نشد'}, status=404)

            product_image_url = request.build_absolute_uri(product.image.url) if product.image else None

            item, created = CartItem.objects.update_or_create(
                cart=cart,
                product_id=product.id,
                defaults={
                    'product_name': product.name,
                    'product_price': product.price,
                    'quantity': request.data.get('quantity', 1),
                    'product_image': product_image_url,
                }
            )

            cart.total_price = sum(item.product_price * item.quantity for item in cart.items.all())
            cart.save()

            serializer = CartSerializer(cart)

            response_data = serializer.data
            for item in response_data['items']:
                item['product_price'] = float(item['product_price'])
                item['price'] = float(item['price'])

            return Response(response_data)

        except AuthenticationFailed:
            cart_data = self.get_cart_from_cookie(request)
            product_id = request.data['product']

            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                return Response({'error': 'محصول یافت نشد'}, status=404)

            product_image_url = request.build_absolute_uri(product.image.url) if product.image else None
            items = cart_data['items']
            updated = False
            for item in items:
                if item['product'] == product_id:
                    item['quantity'] += request.data.get('quantity', 1)
                    updated = True
                    break
            if not updated:
                items.append({
                    'product': product.id,
                    'product_name': product.name,
                    'product_price': product.price,
                    'product_image': product_image_url,
                    'quantity': request.data.get('quantity', 1)
                })
            cart_data['items'] = items

            for item in cart_data['items']:
                item['product_price'] = float(item['product_price'])
                item['price'] = float(item['product_price']) * item['quantity']

            response = Response({'message': 'Cart updated in cookie'})
            response.set_cookie('cart', json.dumps(cart_data, cls=DecimalEncoder), httponly=True)
            return response

    def delete(self, request):
        try:
            user_id = self.get_user_from_token(request)
            product_id = request.data.get('product')

            cart = Cart.objects.filter(customer_id=user_id, is_active=True).first()
            if not cart:
                return Response({'error': 'سبد خرید یافت نشد'}, status=404)

            cart_item = cart.items.filter(product_id=product_id).first()
            if cart_item:
                cart_item.delete()
                cart.total_price = sum(item.product_price * item.quantity for item in cart.items.all())
                cart.save()
            serializer = CartSerializer(cart)
            return Response(serializer.data)

        except AuthenticationFailed:
            cart_data = self.get_cart_from_cookie(request)
            product_id = request.data.get('product')
            cart_data['items'] = [item for item in cart_data['items'] if item['product'] != product_id]

            response = Response({'message': 'Cart updated in cookie', 'items': cart_data['items']})
            response.set_cookie('cart', json.dumps(cart_data), httponly=True)
            return response