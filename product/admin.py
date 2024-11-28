from django.contrib import admin
from .models import Category, Attribute, Product, ProductComment, ProductAttribute

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'parent_category')
    search_fields = ('name',)
    list_filter = ('parent_category',)

class AttributeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock_quantity', 'image')
    search_fields = ('name', 'category__name')
    list_filter = ('category',)
    list_editable = ('price', 'stock_quantity')

class ProductCommentAdmin(admin.ModelAdmin):
    list_display = ('product', 'customer', 'rating', 'status')
    list_filter = ('status',)
    search_fields = ('product__name', 'customer__username')

class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ('product', 'attribute', 'value')
    search_fields = ('product__name', 'attribute__name')

admin.site.register(Category, CategoryAdmin)
admin.site.register(Attribute, AttributeAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductComment, ProductCommentAdmin)
admin.site.register(ProductAttribute, ProductAttributeAdmin)
