from django.urls import path

from . import views

urlpatterns = [
    path('', views.book_favourite, name='book_favourite'),
]
