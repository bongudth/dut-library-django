from django.urls import path
from . import views

app_name = 'books'

urlpatterns = [
    path('', views.home, name='home'),
    path('books/', views.book_all, name='book_all'),
    path('books/search', views.book_searching, name='book_search'),
    path('books/<slug:slug>/', views.book_detail, name='book_detail'),
    path('category/<slug:slug>/', views.book_filter_by_category, name='book_filter_by_category'),
    path('favourite/', views.favourite_all, name='favourite_all'),
    path('favourite/add/', views.favourite_add, name='favourite_add'),
    path('favourite/delete/', views.favourite_delete, name='favourite_delete'),
    path('history/', views.history_of_user, name='history_of_user'),
]
