from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet,
    AttributeViewSet,
    ProductViewSet,
    ProductImageViewSet,
    ProductCommentViewSet,
    ProductAttributeViewSet,
    SiteInfoViewSet,
)


router = DefaultRouter()
# Product
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'attributes', AttributeViewSet, basename='attribute')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'product-images', ProductImageViewSet, basename='productimage')
router.register(r'product-comments', ProductCommentViewSet, basename='productcomment')
router.register(r'product-attributes', ProductAttributeViewSet, basename='productattribute')

# Core
router.register(r'site-info', SiteInfoViewSet, basename='siteinfo')

urlpatterns = router.urls
