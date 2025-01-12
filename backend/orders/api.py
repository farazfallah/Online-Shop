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
        """
        Update cart items with latest product prices from database
        """
        total_price = Decimal('0')
        for item in cart.items.all():
            try:
                product = Product.objects.get(id=item.product_id)
                # محاسبه قیمت جدید با تخفیف
                new_price = product.price - (product.price * Decimal(product.discount) / 100)
                
                # اگر قیمت تغییر کرده باشد، آپدیت می‌کنیم
                if item.product_price != new_price:
                    item.product_price = new_price
                    item.product_name = product.name  # به روز رسانی نام محصول
                    if product.image:
                        item.product_image = product.image.url
                    item.save()
                
                total_price += new_price * item.quantity
            except Product.DoesNotExist:
                continue
        
        cart.total_price = total_price
        cart.save()
        return cart

    def get_cart_from_cookie(self, request):
        """
        Retrieve cart data from cookies and update prices
        """
        cart_data = request.COOKIES.get('cart')
        if cart_data:
            cart_data = json.loads(cart_data)
            updated_items = []
            
            for item in cart_data['items']:
                try:
                    product = Product.objects.get(id=item['product'])
                    # محاسبه قیمت جدید با تخفیف
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
            
            cart_data['items'] = updated_items
            return cart_data
        return {'items': []}

    def get(self, request):
        try:
            user_id = self.get_user_from_token(request)
            cart, _ = Cart.objects.get_or_create(customer_id=user_id, is_active=True)
            
            # به‌روزرسانی قیمت‌ها قبل از ارسال پاسخ
            cart = self.update_cart_prices(cart)
            
            serializer = CartSerializer(cart)
            return Response(serializer.data)
        except AuthenticationFailed:
            cart_data = self.get_cart_from_cookie(request)
            
            # ذخیره قیمت‌های به‌روز شده در کوکی
            response = Response({'id': None, 'customer': None, 'items': cart_data['items']})
            response.set_cookie('cart', json.dumps(cart_data, cls=DecimalEncoder), httponly=True)
            return response

    def post(self, request):
        try:
            user_id = self.get_user_from_token(request)
            cart, _ = Cart.objects.get_or_create(customer_id=user_id, is_active=True)
            product_id = request.data['product']

            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                return Response({'error': 'محصول یافت نشد'}, status=404)

            # محاسبه قیمت با تخفیف
            discount_price = product.price - (product.price * Decimal(product.discount) / 100)
            product_image_url = request.build_absolute_uri(product.image.url) if product.image else None

            try:
                # بررسی وجود محصول در سبد خرید
                cart_item = CartItem.objects.get(cart=cart, product_id=product.id)
                # به‌روزرسانی اطلاعات محصول
                cart_item.product_name = product.name
                cart_item.product_price = discount_price
                cart_item.product_image = product_image_url
                cart_item.quantity = cart_item.quantity + request.data.get('quantity', 1)
                cart_item.save()
            except CartItem.DoesNotExist:
                # ایجاد آیتم جدید
                cart_item = CartItem.objects.create(
                    cart=cart,
                    product_id=product.id,
                    product_name=product.name,
                    product_price=discount_price,
                    quantity=request.data.get('quantity', 1),
                    product_image=product_image_url,
                )

            # به‌روزرسانی قیمت کل سبد خرید
            cart.total_price = sum(item.product_price * item.quantity for item in cart.items.all())
            cart.save()

            serializer = CartSerializer(cart)
            response_data = serializer.data
            
            # تبدیل اعداد اعشاری به float برای JSON
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

            # محاسبه قیمت با تخفیف
            discount_price = product.price - (product.price * Decimal(product.discount) / 100)
            product_image_url = request.build_absolute_uri(product.image.url) if product.image else None
            
            items = cart_data['items']
            updated = False

            # به‌روزرسانی یا اضافه کردن محصول به سبد خرید
            for item in items:
                if item['product'] == product_id:
                    # به‌روزرسانی کامل اطلاعات محصول
                    item['product_name'] = product.name
                    item['product_price'] = float(discount_price)
                    item['product_image'] = product_image_url
                    item['quantity'] += request.data.get('quantity', 1)
                    item['price'] = float(discount_price) * item['quantity']
                    updated = True
                    break

            if not updated:
                # اضافه کردن محصول جدید
                items.append({
                    'product': product.id,
                    'product_name': product.name,
                    'product_price': float(discount_price),
                    'product_image': product_image_url,
                    'quantity': request.data.get('quantity', 1),
                    'price': float(discount_price) * request.data.get('quantity', 1)
                })

            cart_data['items'] = items

            response = Response({'message': 'Cart updated in cookie', 'items': items})
            response.set_cookie('cart', json.dumps(cart_data, cls=DecimalEncoder), httponly=True)
            return response

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