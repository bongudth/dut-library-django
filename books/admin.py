from django.contrib import admin
from django.db.models import Count
import datetime
from .models import Category, Book, History

# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'category', 'author',
                    'description', 'image_url', 'quantity', 'created_at', 'updated_at']
    list_filter = ['category', 'created_at']
    search_fields = ['title', 'author']
    prepopulated_fields = {'slug': ('title',)}


@admin.action(description='Return selected books')
def return_books(modeladmin, request, queryset):
    history = queryset.filter(date_returned__isnull=True).values('book').annotate(book_count=Count('book'))
    
    for book in history:
        book_obj = Book.objects.get(id=book['book'])
        book_obj.quantity += book['book_count']
        book_obj.save()
        
    queryset.filter(date_returned__isnull=True).update(date_returned=datetime.datetime.now())
         


@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):
    list_display = ['book', 'user', 'date_borrowed',
                    'date_expired', 'date_returned']
    list_filter = ['book', 'user']
    search_fields = ['user__username', 'book__title']
    actions = [return_books]
