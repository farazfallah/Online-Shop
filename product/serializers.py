from rest_framework import serializers
from .models import Product, ProductAttribute

class ProductAttributeSerializer(serializers.ModelSerializer):
    attribute_name = serializers.CharField(source='attribute.name', read_only=True)

    class Meta:
        model = ProductAttribute
        fields = ['attribute_name', 'value']


class ProductSerializer(serializers.ModelSerializer):
    final_price = serializers.SerializerMethodField()
    category_breadcrumb = serializers.SerializerMethodField()
    attributes = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['name', 'price', 'discount', 'final_price', 'category_breadcrumb', 'attributes']

    def get_final_price(self, obj):
        return float(obj.price) * (1 - float(obj.discount) / 100)

    def get_category_breadcrumb(self, obj):
        breadcrumb_items = []
        current_category = obj.category

        while current_category:
            breadcrumb_items.append(current_category.name)
            current_category = current_category.parent_category

        breadcrumb_items.reverse()
        return breadcrumb_items

    def get_attributes(self, obj):
        attributes = obj.attributes.all()
        return ProductAttributeSerializer(attributes, many=True).data

