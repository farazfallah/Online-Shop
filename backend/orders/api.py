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

    def update_cart_prices(self, cart):
        total_price = Decimal('0')
        items_to_remove = []
        items_to_update = []
        
        for item in cart.items.all():
            try:
                product = Product.objects.get(id=item.product_id)
                
                if product.stock_quantity == 0:
                    items_to_remove.append(item)
                    continue
                
                if item.quantity > product.stock_quantity:
                    item.quantity = product.stock_quantity
                    items_to_update.append(item)
                    
                new_price = product.price - (product.price * Decimal(product.discount) / 100)
                
                if item.product_price != new_price:
                    item.product_price = new_price
                    item.product_name = product.name
                    if product.image:
                        item.product_image = product.image.url
                    item.save()
                elif item in items_to_update:
                    item.save()
                
                total_price += new_price * item.quantity
                
            except Product.DoesNotExist:
                items_to_remove.append(item)
                continue
        
        for item in items_to_remove:
            item.delete()
        
        cart.total_price = total_price
        cart.save()
        return cart

    def get_cart_from_cookie(self, request):
        """
        Retrieve cart data from cookies and update prices,
        removing out of stock products
        """
        try:
            cart_data = request.COOKIES.get('cart')
            if not cart_data:
                return {'items': []}

            try:
                cart_data = json.loads(cart_data.replace('\\', ''))
            except json.JSONDecodeError:
                return {'items': []}

            updated_items = []
            
            for item in cart_data.get('items', []):
                try:
                    product = Product.objects.get(id=item['product'])
                    
                    if product.stock_quantity == 0:
                        continue
                        
                    new_price = float(product.price - (product.price * Decimal(product.discount) / 100))
                    
                    item.update({
                        'product_name': product.name,
                        'product_price': new_price,
                        'product_image': request.build_absolute_uri(product.image.url) if product.image else None,
                        'price': new_price * item['quantity']
                    })
                    updated_items.append(item)
                except Product.DoesNotExist:
                    continue
                except KeyError:
                    continue
                
            cart_data['items'] = updated_items
            return cart_data
        except Exception:
            return {'items': []}

    def get(self, request):
        try:
            user_id = self.get_user_from_token(request)
            cart, _ = Cart.objects.get_or_create(customer_id=user_id, is_active=True)
            cart = self.update_cart_prices(cart)
            serializer = CartSerializer(cart)
            return Response(serializer.data)
        except AuthenticationFailed:
            try:
                cart_data = self.get_cart_from_cookie(request)
                response = Response({
                    'id': None,
                    'customer': None,
                    'session_id': None,
                    'total_price': sum(item.get('price', 0) for item in cart_data.get('items', [])),
                    'is_active': True,
                    'items': cart_data.get('items', [])
                })
                
                response.set_cookie(
                    'cart',
                    json.dumps(cart_data, cls=DecimalEncoder),
                    httponly=True
                )
                return response
            except Exception as e:
                print(f"Error processing cart cookie: {str(e)}")
                return Response({
                    'id': None,
                    'customer': None,
                    'session_id': None,
                    'total_price': 0,
                    'is_active': True,
                    'items': []
                })

    def post(self, request):
        try:
            user_id = self.get_user_from_token(request)
            cart, _ = Cart.objects.get_or_create(customer_id=user_id, is_active=True)
            product_id = request.data['product']
            requested_quantity = int(request.data.get('quantity', 1))

            try:
                product = Product.objects.get(id=product_id)
                
                if product.stock_quantity == 0:
                    return Response(
                        {'error': 'محصول در حال حاضر ناموجود است'}, 
                        status=400
                    )

                discount_price = product.price - (product.price * Decimal(product.discount) / 100)
                product_image_url = request.build_absolute_uri(product.image.url) if product.image else None

                try:
                    cart_item = CartItem.objects.get(cart=cart, product_id=product.id)
                    new_quantity = cart_item.quantity + requested_quantity
                    
                    if new_quantity > product.stock_quantity:
                        return Response(
                            {'error': f'موجودی محصول {product.stock_quantity} عدد است. نمی‌توانید بیش از این تعداد سفارش دهید.'}, 
                            status=400
                        )
                    
                    cart_item.product_name = product.name
                    cart_item.product_price = discount_price
                    cart_item.product_image = product_image_url
                    cart_item.quantity = new_quantity
                    cart_item.save()
                
                except CartItem.DoesNotExist:
                    if requested_quantity > product.stock_quantity:
                        return Response(
                            {'error': f'موجودی محصول {product.stock_quantity} عدد است. نمی‌توانید بیش از این تعداد سفارش دهید.'}, 
                            status=400
                        )
                    
                    cart_item = CartItem.objects.create(
                        cart=cart,
                        product_id=product.id,
                        product_name=product.name,
                        product_price=discount_price,
                        quantity=requested_quantity,
                        product_image=product_image_url,
                    )

                cart.total_price = sum(item.product_price * item.quantity for item in cart.items.all())
                cart.save()

                serializer = CartSerializer(cart)
                response_data = serializer.data
                
                for item in response_data['items']:
                    item['product_price'] = float(item['product_price'])
                    item['price'] = float(item['price'])

                return Response(response_data)

            except Product.DoesNotExist:
                return Response({'error': 'محصول یافت نشد'}, status=404)

        except AuthenticationFailed:
            cart_data = self.get_cart_from_cookie(request)
            product_id = request.data['product']
            requested_quantity = int(request.data.get('quantity', 1))

            try:
                product = Product.objects.get(id=product_id)
                
                if product.stock_quantity == 0:
                    return Response(
                        {'error': 'محصول در حال حاضر ناموجود است'}, 
                        status=400
                    )
                    
                discount_price = product.price - (product.price * Decimal(product.discount) / 100)
                product_image_url = request.build_absolute_uri(product.image.url) if product.image else None
                
                items = cart_data['items']
                updated = False

                for item in items:
                    if item['product'] == product_id:
                        new_quantity = item['quantity'] + requested_quantity
                        
                        if new_quantity > product.stock_quantity:
                            return Response(
                                {'error': f'موجودی محصول {product.stock_quantity} عدد است. نمی‌توانید بیش از این تعداد سفارش دهید.'}, 
                                status=400
                            )
                            
                        item['product_name'] = product.name
                        item['product_price'] = float(discount_price)
                        item['product_image'] = product_image_url
                        item['quantity'] = new_quantity
                        item['price'] = float(discount_price) * new_quantity
                        updated = True
                        break

                if not updated:
                    if requested_quantity > product.stock_quantity:
                        return Response(
                            {'error': f'موجودی محصول {product.stock_quantity} عدد است. نمی‌توانید بیش از این تعداد سفارش دهید.'}, 
                            status=400
                        )
                        
                    items.append({
                        'product': product.id,
                        'product_name': product.name,
                        'product_price': float(discount_price),
                        'product_image': product_image_url,
                        'quantity': requested_quantity,
                        'price': float(discount_price) * requested_quantity
                    })

                cart_data['items'] = items

                response = Response({'message': 'Cart updated in cookie', 'items': items})
                response.set_cookie('cart', json.dumps(cart_data, cls=DecimalEncoder), httponly=True)
                return response
                
            except Product.DoesNotExist:
                return Response({'error': 'محصول یافت نشد'}, status=404)

    def delete(self, request):
        try:
            user_id = self.get_user_from_token(request)
            product_id = request.query_params.get('product') or request.data.get('product')

            if not product_id:
                return Response({'error': 'شناسه محصول الزامی است'}, status=400)

            cart = Cart.objects.filter(customer_id=user_id, is_active=True).first()
            if not cart:
                return Response({'error': 'سبد خرید یافت نشد'}, status=404)

            cart_item = cart.items.filter(product=product_id).first()
            if not cart_item:
                return Response({'error': 'آیتم در سبد خرید یافت نشد'}, status=404)

            cart_item.delete()
            cart.total_price = sum(item.product_price * item.quantity for item in cart.items.all())
            cart.save()

            serializer = CartSerializer(cart)
            return Response(serializer.data)

        except AuthenticationFailed:
            cart_data = self.get_cart_from_cookie(request)
            product_id = request.query_params.get('product') or request.data.get('product')

            if not product_id:
                return Response({'error': 'شناسه محصول الزامی است'}, status=400)

            cart_data['items'] = [item for item in cart_data['items'] if str(item['product']) != str(product_id)]

            response = Response({'message': 'آیتم از سبد خرید حذف شد', 'items': cart_data['items']})
            response.set_cookie('cart', json.dumps(cart_data), httponly=True)
            return response