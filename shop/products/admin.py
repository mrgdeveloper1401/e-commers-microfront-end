from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from .models import Option, OptionGroup, OptionGroupValue, ProductClass, ProductAttribute \
    ,ProductAttributeValue, Product, ProductRecomendation, ProductImage
from inventory.admin import StockRecordInline


class ProductAttributeInline(admin.TabularInline):
    model = ProductAttribute
    extra = 1

class RecomendationProductInline(admin.TabularInline):
    model = ProductRecomendation
    extra = 1
    fk_name = 'primary'

class ProductAttributeValueInline(admin.TabularInline):
    model = ProductAttributeValue
    extra = 1
    
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    pass


@admin.register(OptionGroup)
class OptionGroupAdmin(admin.ModelAdmin):
    pass


@admin.register(OptionGroupValue)
class OptionGroupValueAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
    pass


class AttributeCountfilter(admin.SimpleListFilter):
    parameter_name = 'attribute_count'
    title = 'attribute count'
    
    def lookups(self, request: Any, model_admin: Any):
        return (
            ('more', 'more then 5'),
            ('less', 'lower than 5'),
        )
        
    def queryset(self, request: Any, queryset: QuerySet[Any]) -> QuerySet[Any] | None:
        if self.value == 'more':
            return queryset.filter(attribute_count__gt=5)
        if self.value == 'less':
            return queryset.filter(attribute_count__lt=5)


@admin.register(ProductClass)
class ProductClassAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_stock','requires_shipping', 'has_attribute', 'attribute_count')
    list_filter = ('is_stock','requires_shipping', AttributeCountfilter)
    inlines = (ProductAttributeInline,)
    actions = ('enable_is_stock', 'disable_is_stock', 'enable_require_shipping', 'disable_is_require_shipping')
    prepopulated_fields = {'slug': ('title',)}
    
    def enable_is_stock(self, request, queryset):
        queryset.update(is_stock=True)
        
    def disable_is_stock(self, request, queryset):
        queryset.update(is_stock=False)
        
    def enable_require_shipping(self, request, queryset):
        queryset.update(requires_shipping=True)

    def disable_is_require_shipping(self, request, queryset):
        queryset.update(requires_shipping=False)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = (RecomendationProductInline, StockRecordInline, ProductAttributeValueInline \
        , ProductImageInline)


@admin.register(ProductAttributeValue)
class ProductAttributeValueAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    pass