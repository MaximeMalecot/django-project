from django.urls import path

from . import views

urlpatterns = [
    path('books', views.library_books, name='library_books'),
]