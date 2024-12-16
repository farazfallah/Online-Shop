from rest_framework.viewsets import ModelViewSet
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


# Core
class SiteInfoViewSet(ModelViewSet):
    queryset = SiteInfo.objects.all()
    serializer_class = SiteInfoSerializer
