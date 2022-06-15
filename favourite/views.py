from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from books.models import Book
from .favourite import Favourite

# Create your views here.

def book_favourite(request):
    return render(request, 'library/favourite/favourite.html')

def favourite_add(request):
    favourite = Favourite(request)
    if request.POST.get('action') == 'post':
        book_id = int(request.POST.get('book_id'))
        book = get_object_or_404(Book, id=book_id)
        favourite.add(book=book)
        response = JsonResponse({'status': 'success'})
        return response
