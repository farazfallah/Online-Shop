from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import RetrieveAPIView, ListAPIView
from django_filters.rest_framework import DjangoFilterBackend, FilterSet
from rest_framework.filters import SearchFilter, OrderingFilter
from product.models import (
    Category,
    Attribute,
    Product,
    ProductImage,
    ProductComment,
    ProductAttribute,
)
from core.models import SiteInfo
from api.serializers import (
    CategorySerializer,
    AttributeSerializer,
    ProductSerializer,
    ProductImageSerializer,
    ProductCommentSerializer,
    ProductAttributeSerializer,
    ProductsByCategorySerializer,
    SiteInfoSerializer,
)


# Products
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

# Core
class SiteInfoViewSet(ModelViewSet):
    queryset = SiteInfo.objects.all()
    serializer_class = SiteInfoSerializer


# Search API
class ProductSearchView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    search_fields = ['name', 'description', 'category__name', 'attributes__value']
    ordering_fields = ['price', 'stock_quantity', 'discount']
    filterset_fields = ['category', 'price', 'stock_quantity', 'discount']