from email import message
from gc import get_objects
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
import datetime
from .models import Category, Book, History

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


def book_searching(request):
    keyword = request.GET.get('keyword')
    books = Book.objects.filter(title__icontains=keyword)
    context = {
        'keyword': keyword,
        'books': books.order_by('title'),
    }

    return render(request, 'library/books/index.html', context)


def favourite_all(request):
    books = request.user.favourite_books.all()
    return render(request, 'library/favourite/favourite.html', {'books': books})


def favourite_add(request):
    if request.POST.get('action') == 'POST':
        book_id = int(request.POST.get('book_id'))
        book = get_object_or_404(Book, id=book_id)
        book.favourite.add(request.user)
        favourite_quantity = request.user.favourite_books.all().count()
        response = JsonResponse({'favourite_quantity': favourite_quantity})
        return response


def favourite_delete(request):
    if request.POST.get('action') == 'POST':
        book_id = int(request.POST.get('book_id'))
        book = get_object_or_404(Book, id=book_id)
        book.favourite.remove(request.user)
        favourite_quantity = request.user.favourite_books.all().count()
        response = JsonResponse({'favourite_quantity': favourite_quantity})
        return response


def history_of_user(request):
    if request.method == 'POST':
        book_id = request.POST.get('book_id')
        book = get_object_or_404(Book, id=book_id)
        print(book)
        
        if book.quantity > 0: 
            user = request.user
            history = History(user=user, book=book, date_expired=datetime.datetime.now() + datetime.timedelta(days=7))
            history.save()
            book.quantity -= 1
            book.save()
            message = "You have successfully borrowed the book."
        else:
            message = "Sorry, this book is not available."
            
        return JsonResponse({'message': message})
    
    history = History.objects.filter(user=request.user)
    context = {
        'history': history
    }

    return render(request, 'library/history/index.html', context)
