from django.http import HttpResponse
from django.shortcuts import render
from .models import Book

def library_books(request):
    books = Book.objects.all()
    return render(request, 'library/index.html', {'books': books})

# def books(request):
#     books = Book.objects.all()
#     return render(request, 'library/books.html', {'books': books})