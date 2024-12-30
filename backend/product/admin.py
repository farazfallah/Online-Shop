from django.contrib import admin
from .models import Category, Attribute, Product, ProductComment, ProductAttribute, ProductImage
from django.utils.html import format_html


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'icon', 'image', 'parent_category', 'is_active')
    search_fields = ('name',)
    list_filter = ('parent_category', 'is_active')
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'icon', 'image', 'parent_category', 'is_active'),
        }),
    )


class ProductAttributeInline(admin.TabularInline):
    model = ProductAttribute
    extra = 1


class AttributeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'discount', 'stock_quantity', 'image')
    search_fields = ('name', 'category__name')
    list_filter = ('category',)
    list_editable = ('price', 'discount', 'stock_quantity')
    inlines = [ProductImageInline, ProductAttributeInline]
    
    
class ProductCommentAdmin(admin.ModelAdmin):
    list_display = ('product', 'customer', 'rating', 'status')
    list_filter = ('status',)
    search_fields = ('product__name', 'customer__username')

admin.site.register(Category, CategoryAdmin)
admin.site.register(Attribute, AttributeAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductComment, ProductCommentAdmin)
