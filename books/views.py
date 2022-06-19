from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Category, Book

# Create your views here.


@login_required(login_url='/auth/login')
def home(request):
    books = Book.objects.all()
    return render(request, 'library/home.html', {'books': books})


def book_all(request):
    books = Book.objects.all().order_by('title')
    return render(request, 'library/books/index.html', {'books': books})


def book_detail(request, slug):
    book = get_object_or_404(Book, slug=slug)
    return render(request, 'library/books/detail.html', {'book': book})


def book_filter_by_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    books = Book.objects.filter(category=category).order_by('title')
    return render(request, 'library/books/category.html', {'category': category, 'books': books})


def book_searching(req):
    keyword = req.GET.get('keyword')
    books = Book.objects.filter(title__icontains=keyword)
    context = {
        'keyword': keyword,
        'books': books.order_by('title'),
    }
    
    return render(req, 'library/books/index.html', context)
