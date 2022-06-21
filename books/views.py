from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count
import datetime
from .models import Category, Book, History

# Create your views here.


@login_required(login_url='/auth/login')
def home(request):
    history = History.objects.values('book').annotate(
        book_count=Count('book')).order_by('-book_count')[:3]
    books = Book.objects.filter(id__in=history.values('book'))

    return render(request, 'library/home.html', {'books': books})


@login_required(login_url='/auth/login')
def book_all(request):
    books = Book.objects.all().order_by('title')
    return render(request, 'library/books/index.html', {'books': books})


@login_required(login_url='/auth/login')
def book_detail(request, slug):
    book = get_object_or_404(Book, slug=slug)
    is_favourite = book.favourite.filter(id=request.user.id).exists()
    context = {
        'book': book,
        'is_favourite': is_favourite,
    }
    return render(request, 'library/books/detail.html', context)


@login_required(login_url='/auth/login')
def book_filter_by_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    books = Book.objects.filter(category=category).order_by('title')
    return render(request, 'library/books/category.html', {'category': category, 'books': books})


@login_required(login_url='/auth/login')
def book_searching(request):
    keyword = request.GET.get('keyword')
    books = Book.objects.filter(title__icontains=keyword)
    context = {
        'keyword': keyword,
        'books': books.order_by('title'),
    }

    return render(request, 'library/books/index.html', context)


@login_required(login_url='/auth/login')
def favourite_all(request):
    books = request.user.favourite_books.all()
    return render(request, 'library/favourite/favourite.html', {'books': books})


@login_required(login_url='/auth/login')
def favourite_add(request):
    if request.POST.get('action') == 'POST':
        book_id = int(request.POST.get('book_id'))
        book = get_object_or_404(Book, id=book_id)
        book.favourite.add(request.user)
        favourite_quantity = request.user.favourite_books.all().count()
        is_favourite = book.favourite.filter(id=request.user.id).exists()
        context = {
            'favourite_quantity': favourite_quantity,
            'is_favourite': is_favourite,
        }
        response = JsonResponse(context)
        return response


@login_required(login_url='/auth/login')
def favourite_delete(request):
    if request.POST.get('action') == 'POST':
        book_id = int(request.POST.get('book_id'))
        book = get_object_or_404(Book, id=book_id)
        book.favourite.remove(request.user)
        favourite_quantity = request.user.favourite_books.all().count()
        is_favourite = book.favourite.filter(id=request.user.id).exists()
        context = {
            'favourite_quantity': favourite_quantity,
            'is_favourite': is_favourite,
        }
        response = JsonResponse(context)
        return response


@login_required(login_url='/auth/login')
def history_of_user(request):
    if request.method == 'POST':
        book_id = request.POST.get('borrowed')
        book = get_object_or_404(Book, id=book_id)

        if book.is_in_stock:
            user = request.user
            history = History(user=user, book=book, date_expired=datetime.datetime.now(
            ) + datetime.timedelta(days=7))
            history.save()
            book.quantity -= 1
            book.save()
            message = "You have successfully borrowed the book."
        else:
            message = "Sorry, this book is not available."

    history = History.objects.filter(user=request.user)
    history_quantity = history.count()
    context = {
        'history': history,
        'history_quantity': history_quantity
    }

    return render(request, 'library/history/index.html', context)
