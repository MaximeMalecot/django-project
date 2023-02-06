from django.http import HttpResponse
from django.shortcuts import  render, redirect
from .models import Book, Book_Reference
from .forms import RegisterForm
from django.contrib.auth import login
from django.contrib import messages

#Displays every Books references
def index(request):
    books = Book_Reference.objects.all()
    return render(request, 'library/index.html', {'books': books})

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful." )
            return redirect("library:home")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = RegisterForm()
    return render (request=request, template_name="register.html", context={"register_form":form})


def books(request):
    books = Book_Reference.objects.all()
    return render(request, 'library/index.html', {'books': books})

def book_reference(request, book_id):
    book = Book_Reference.objects.get(pk=book_id)
    if book is None:
        raise Http404("Book reference does not exist")
    availabilities = Book.objects.filter(reference=book, stock__gt=0)
    return render(request, 'library/book.html', {'book': book, 'availabilities': availabilities})

def borrow_book(request, book_id):
    book = Book.objects.get(pk=book_id)
    if book is None:
        raise Http404("Book does not exist")
    if book.stock <= 0:
        raise Http404("Book is not available")
        
    book.stock = book.stock - 1
    book.save()
    return render(request, 'library/borrowed.html', {'book': book})