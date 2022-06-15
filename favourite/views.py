from django.shortcuts import render

# Create your views here.

def book_favourite(request):
    return render(request, 'library/favourite/favourite.html')
