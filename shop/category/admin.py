from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from .models import Category, Categoryproxy


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('category_name',)}
    search_fields = ('category_name',)
    list_display = ('category_name', 'is_publish', 'parent')
    list_per_page = 10
    list_filter = ('is_publish', )
    actions = ('disable_category', )
    
    def disable_category(self, request, queryset):
        queryset.update(is_publish=False)

    

class CategoryInline(admin.TabularInline):
    model = Category
    extra = 1


@admin.register(Categoryproxy)
class CategoryproxyAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'is_publish', 'parent')
    actions = ('enable_category',)
    
    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).filter(is_publish=False)
    
    def enable_category(self, request, queryset):
        queryset.update(is_publish=True)