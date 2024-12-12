from django.contrib import admin
from .models import Category, Attribute, Product, ProductComment, ProductAttribute, ProductImage
from django.utils.html import format_html


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'icon', 'image', 'parent_category')
    search_fields = ('name',)
    list_filter = ('parent_category',)
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'icon', 'image', 'parent_category'),
            'description': (
                "For the 'icon' field, enter the class name of a Bootstrap Icon. "
                "For example: <code>bi bi-tablet</code>. "
                "You can browse the full list of icons at "
                "<a href='https://icons.getbootstrap.com/' target='_blank'>Bootstrap Icons</a>."
            ),
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
