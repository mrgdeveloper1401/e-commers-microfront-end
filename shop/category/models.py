from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from .manager import CategortPublisher
from core.models import AuditableModel


class Category(MPTTModel, AuditableModel):
    category_name = models.CharField(max_length=50, db_index=True)
    slug = models.SlugField(allow_unicode=True, unique=True)
    is_publish = models.BooleanField(default=True)
    parent = TreeForeignKey('self', on_delete=models.PROTECT, null=True, blank=True, related_name='children')
    
    def __str__(self) -> str:
        return self.category_name

    objects = CategortPublisher()
    
    class MPTTMeta:
        db_table = 'category'
        order_insertion_by = ('-category_name',)
        
    
class Categoryproxy(Category):
    class Meta:
        proxy = True