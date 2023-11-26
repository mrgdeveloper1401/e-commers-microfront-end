from typing import Any
from django.db import models
from django.utils.translation import gettext_lazy as _


class OptionGroup(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.title


class OptionGroupValue(models.Model):
    title = models.CharField(max_length=100)
    group = models.ForeignKey(OptionGroup, on_delete=models.CASCADE, related_name='values')

    def __str__(self) -> str:
        return self.title


class ProductClass(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, allow_unicode=True)
    description = models.TextField(blank=True, null=True)
    is_stock = models.BooleanField(default=True)
    requires_shipping = models.BooleanField(default=True)
    options = models.ManyToManyField('Option', blank=True)

    def has_attribute(self):
        return self.attributes.exists()

    def attribute_count(self):
        return self.attributes.count()

    def __str__(self) -> str:
        return self.title


class ProductAttribute(models.Model):
    class AttributeTypeChoose(models.TextChoices):
        TEXT = 'text'
        INTEGER = 'integer'
        FLOAT = 'float'
        OPTION = 'option'
        MULTI_OPTION = 'multi_option'

    title = models.CharField(max_length=100)
    product_class = models.ForeignKey(ProductClass, on_delete=models.CASCADE, null=True, related_name='attributes')
    types = models.CharField(max_length=12, choices=AttributeTypeChoose.choices, default=AttributeTypeChoose.TEXT)
    required = models.BooleanField(default=False)
    option_group = models.ForeignKey(OptionGroup, on_delete=models.PROTECT, null=True, blank=True)


class Option(models.Model):
    class OptionTypeChoose(models.TextChoices):
        TEXT = 'text'
        INTEGER = 'integer'
        FLOAT = 'float'
        OPTION = 'option'
        MULTI_OPTION = 'multi_option'

    title = models.CharField(max_length=100)
    types = models.CharField(max_length=12, choices=OptionTypeChoose.choices, default=OptionTypeChoose.TEXT)
    required = models.BooleanField(default=False)


class Product(models.Model):
    class ProductTypeChoose(models.TextChoices):
        STANDALONE = 'standalone'
        PARENT = 'parent'
        CHILD = 'child'

    structure = models.CharField(max_length=10, choices=ProductTypeChoose.choices, default=ProductTypeChoose.STANDALONE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children', blank=True, null=True)
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    upc = models.CharField(max_length=24, blank=True, null=True)
    sku = models.CharField(max_length=13, blank=True, null=True)
    is_public = models.BooleanField(default=True)
    meta_title = models.CharField(max_length=128, null=True, blank=True)
    meta_description = models.TextField(null=True, blank=True)
    product_class = models.ForeignKey(ProductClass, on_delete=models.PROTECT, blank=True, null=True, related_name='products')
    attributes = models.ManyToManyField(ProductAttribute, through='ProductAttributeValue')
    recommender_system = models.ManyToManyField('self', through='ProductRecomendation')
    category = models.ManyToManyField('category.Category', blank=True, related_name='category_products')
    
    def __str__(self) -> str:
        return self.title
    
    @property
    def main_image(self):
        if self.product_images.exists():
            return self.product_images.first()
        return None

class ProductAttributeValue(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    attribute = models.ForeignKey(ProductAttribute, on_delete=models.CASCADE)
    value_text = models.TextField(blank=True, null=True)
    value_integer = models.IntegerField(blank=True, null=True)
    value_float = models.FloatField(blank=True, null=True)
    value_option = models.ForeignKey(OptionGroupValue, on_delete=models.PROTECT)
    value_multi_option = models.ManyToManyField(OptionGroupValue, related_name='value_multi_options')

    class Meta:
        unique_together = ('product', 'attribute')


class ProductRecomendation(models.Model):
    primary = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='recommendations')
    recommendation = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_recomendation')
    rank = models.PositiveSmallIntegerField(default=0)

    class Meta:
        unique_together = ('primary', 'recommendation')
        ordering = ('primary', '-rank')


class ProductImage(models.Model):
    image = models.ForeignKey('images.image', on_delete=models.CASCADE, related_name='images')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='product_images')
    display_order = models.PositiveIntegerField(default=0)
    
    def __str__(self) -> str:
        return self.product.title
    
    class Meta:
        ordering = ('display_order',)
        
    def delete(self, using: Any = ..., keep_parents: bool = ...) -> tuple[int, dict[str, int]]:
        super().delete(using, keep_parents)
        for index, img in enumerate(self.product_images.all()):
            img.display_order = index
            img.save()
            
    