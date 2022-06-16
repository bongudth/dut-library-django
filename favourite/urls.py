from django.urls import path

from . import views

app_name = 'favourite'

urlpatterns = [
    path('', views.book_favourite, name='book_favourite'),
    path('add/', views.favourite_add, name='favourite_add'),
    path('delete/', views.favourite_delete, name='favourite_delete'),
]
