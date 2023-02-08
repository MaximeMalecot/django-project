from django.http import HttpResponse
from django.shortcuts import  render, redirect
from .models import Book, Book_Reference
from .forms import RegisterUserForm, RegisterLibrarianForm, CreateBookReferenceForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import librarian_required, admin_required

# Default views

def index(request):
    books = Book_Reference.objects.all()
    return render(request, 'library/index.html', {'books': books})

def register(request):
    return render(request, 'register.html')

def register_member(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful." )
            return redirect("library:home")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = RegisterUserForm()
    return render (request=request, template_name="register_form.html", context={"form":form,"role":"member"})

def register_librarian(request):
    if request.method == "POST":
        form = RegisterLibrarianForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful." )
            return redirect("library:home")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = RegisterLibrarianForm()
    return render (request=request, template_name="register_form.html", context={"form":form,"role":"librarian"})

# Books views

def books(request):
    books = Book_Reference.objects.all()
    return render(request, 'library/index.html', {'books': books})

def book_reference(request, book_id):
    book = Book_Reference.objects.get(pk=book_id)
    if book is None:
        raise Http404("Book reference does not exist")
    availabilities = Book.objects.filter(reference=book, stock__gt=0)
    return render(request, 'library/book.html', {'book': book, 'availabilities': availabilities})

@login_required
def borrow_book(request, book_id):
    book = Book.objects.get(pk=book_id)
    if book is None:
        raise Http404("Book does not exist")
    if book.stock <= 0:
        raise Http404("Book is not available")
        
    book.stock = book.stock - 1
    book.save()
    return render(request, 'library/borrowed.html', {'book': book})

@librarian_required
def create_book(request):
    books = Book_Reference.objects.all()
    return render(request, 'library/index.html', {'books': books})

@librarian_required
def create_book_reference(request):
    if request.method == "POST":
        form = CreateBookReferenceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Book reference created." )
            return redirect("library:home")
        messages.error(request, "Invalid form.")
    form = CreateBookReferenceForm()
    return render (request=request, template_name="library/book_reference_form.html", context={"form":form,"type":"create"})

@librarian_required
def edit_book_reference(request, book_reference_id):
    instance = Book_Reference.objects.get(pk=book_reference_id)
    if request.method == "POST":
        form = CreateBookReferenceForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, "Book reference edited." )
            return redirect("library:home")
        messages.error(request, "Invalid form.")
    form = CreateBookReferenceForm(instance=instance)
    return render (request=request, template_name="library/book_reference_form.html", context={"form":form,"type":"edit","book":instance})

