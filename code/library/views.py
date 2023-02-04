from django.http import HttpResponse
from django.shortcuts import render
from .models import Book, Book_Reference

#Displays every Books references
def index(request):
    books = Book_Reference.objects.all()
    return render(request, 'library/index.html', {'books': books})

def book_reference(request, book_id):
    book = Book_Reference.objects.get(pk=book_id)
    if book is None:
        raise Http404("Book does not exist")
    availabilities = Book.objects.filter(reference=book, stock__gt=0)
    return render(request, 'library/book.html', {'book': book, 'availabilities': availabilities})