from django.contrib import admin
from .models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'category_name': ('slug',)}
    search_fields = ('category_name',)
    list_display = ('category_name', 'is_publish', 'parent')


class CategoryInline(admin.TabularInline):
    model = Category
    extra = 1