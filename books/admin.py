from django.contrib import admin
from .models import Category, Book

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'category', 'author', 'description', 'image_url', 'quantity', 'created_at', 'updated_at']
    list_filter = ['category', 'created_at']
    prepopulated_fields = {'slug': ('title',)}