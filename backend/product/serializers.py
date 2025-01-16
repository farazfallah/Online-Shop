from rest_framework import serializers
from django.db.models import Avg
from customers.models import Customer
from product.models import (
    Category,
    Attribute,
    Product,
    ProductImage,
    ProductComment,
    ProductAttribute,
)

class CategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'icon', 'parent_category', 'image', 'subcategories']
    
    def get_subcategories(self, obj):
        return CategorySerializer(obj.subcategories.all(), many=True).data
    

class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = ['id', 'name', 'description']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'product']


class UserCommentSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    profile_image_url = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = ['id', 'full_name', 'profile_image_url']

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()

    def get_profile_image_url(self, obj):
        request = self.context.get('request')
        if obj.image:
            # Use request.build_absolute_uri if request is available
            if request:
                return request.build_absolute_uri(obj.image.url)
            # Fallback to relative URL if no request
            return obj.image.url
        # Return default image URL if no image
        return '/media/users/default.png'

class ProductCommentSerializer(serializers.ModelSerializer):
    customer = UserCommentSerializer(read_only=True)

    class Meta:
        model = ProductComment
        fields = ['id', 'product', 'customer', 'comment', 'rating', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'status', 'created_at', 'updated_at']

    def create(self, validated_data):
        # Ensure we're using the customer ID, not the object
        customer = self.context.get('customer')
        if not customer:
            raise serializers.ValidationError("Customer is required")
        
        # Explicitly set the customer_id
        validated_data['customer_id'] = customer
        
        # Remove 'customer' from validated_data if it exists
        validated_data.pop('customer', None)
        
        return super().create(validated_data)
    

class ProductAttributeSerializer(serializers.ModelSerializer):
    attribute_name = serializers.CharField(source='attribute.name', read_only=True)

    class Meta:
        model = ProductAttribute
        fields = ['id', 'product', 'attribute', 'attribute_name', 'value']


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    comments = ProductCommentSerializer(many=True, read_only=True)
    attributes = ProductAttributeSerializer(many=True, read_only=True)
    
    comments_count = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'category', 'category_name', 'price', 'stock_quantity',
            'image', 'discount', 'images', 'comments', 'attributes', 
            'comments_count', 'average_rating'
        ]

    def get_comments_count(self, obj):
        return obj.comments.filter(status='approved').count()

    def get_average_rating(self, obj):
        return obj.comments.filter(status='approved').aggregate(
            avg_rating=Avg('rating')
        )['avg_rating'] or 0.0


class ProductsByCategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'icon', 'image', 'products']
        