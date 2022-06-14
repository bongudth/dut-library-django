from django.db import models
from django.urls import reverse

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = 'categories'

    def get_absolute_url(self):
        return reverse('books:book_filter_by_category', args=[self.slug])

    def __str__(self):
        return self.name

class Book(models.Model):
    category = models.ForeignKey(Category, related_name='book_category', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image_url = models.URLField(blank=True, default='https://hips.hearstapps.com/hmg-prod/images/old-books-arranged-on-shelf-royalty-free-image-1572384534.jpg?crop=0.668xw:1.00xh;0,0&resize=2048:*')
    slug = models.SlugField(max_length=255, unique=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'books'
        ordering = ('-created_at',)

    def get_absolute_url(self):
        return reverse('books:book_detail', args=[self.slug])

    def __str__(self):
        return self.title
