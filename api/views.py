from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import RetrieveAPIView
from product.models import (
    Category,
    Attribute,
    Product,
    ProductImage,
    ProductComment,
    ProductAttribute,
)
from core.models import SiteInfo
from .serializers import (
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
