from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import RetrieveAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import generics
from rest_framework.filters import SearchFilter
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from core.utils import get_user_from_token
from customers.models import Customer

from product.models import (
    Category,
    Attribute,
    Product,
    ProductImage,
    ProductComment,
    ProductAttribute,
)
from product.serializers import (
    CategorySerializer,
    AttributeSerializer,
    ProductSerializer,
    ProductImageSerializer,
    ProductCommentSerializer,
    ProductAttributeSerializer,
    ProductsByCategorySerializer,
)


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class AttributeViewSet(ModelViewSet):
    queryset = Attribute.objects.all()
    serializer_class = AttributeSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductImageViewSet(ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer


class ProductCommentViewSet(ModelViewSet):
    queryset = ProductComment.objects.all()
    serializer_class = ProductCommentSerializer


class ProductAttributeViewSet(ModelViewSet):
    queryset = ProductAttribute.objects.all()
    serializer_class = ProductAttributeSerializer


class ProductsByCategoryView(RetrieveAPIView):
    queryset = Category.objects.prefetch_related('products').all()
    serializer_class = ProductsByCategorySerializer
    
    
class ProductPagination(PageNumberPagination):
    page_size = 10  # تعداد محصولات در هر صفحه
    page_size_query_param = 'page_size'  # امکان تغییر تعداد محصولات در هر صفحه از طریق URL
    max_page_size = 100  # حداکثر تعداد محصولات در هر صفحه

class ProductSearchView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = ProductPagination  # اضافه کردن کلاس صفحه‌بندی

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['name', 'description', 'category__name', 'attributes__value']
    ordering_fields = ['price', 'stock_quantity', 'discount']
    filterset_fields = ['category', 'price', 'stock_quantity', 'discount']
    

class ProductCommentAPIView(APIView):
    def get(self, product_id):
        product = get_object_or_404(Product, id=product_id)
        comments = product.comments.filter(status='approved')
        serializer = ProductCommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductCommentAPIView(APIView):
    def post(self, request, product_id):
        try:
            user_id = get_user_from_token(request)
            user = Customer.objects.get(id=user_id)  # Get the full user object
        except AuthenticationFailed as e:
            return Response({'detail': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        except Customer.DoesNotExist:
            return Response({'detail': 'کاربر یافت نشد'}, status=status.HTTP_404_NOT_FOUND)

        product = get_object_or_404(Product, id=product_id)
        
        data = request.data.copy()
        data['product'] = product.id
        
        serializer = ProductCommentSerializer(
            data=data, 
            context={
                'customer': user.id,
                'request': request  # Pass request for generating absolute URLs
            }
        )
        
        if serializer.is_valid():
            comment = serializer.save(status='pending', customer=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)