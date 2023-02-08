from django.http import HttpResponse
from django.shortcuts import  render, redirect
from .models import Book, Book_Reference, Genre
from .forms import RegisterUserForm, RegisterLibrarianForm, BookReferenceForm, BookForm, BookEditForm, GenreForm
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
    return render (request=request, template_name="library/forms/register_form.html", context={"form":form,"role":"member"})

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
    return render (request=request, template_name="library/forms/register_form.html", context={"form":form,"role":"librarian"})

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
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.library = request.user.library
            form.save()
            messages.success(request, "Book created." )
            return redirect("library:home")
        messages.error(request, "Invalid form.")
    form = BookForm()
    return render (request=request, template_name="library/forms/book_form.html", context={"form":form,"type":"create"})

@librarian_required
def edit_book(request, book_id):
    instance = Book.objects.get(pk=book_id)
    if request.method == "POST":
        form = BookEditForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, "Book edited." )
            return redirect("library:home")
        messages.error(request, "Invalid form.")
    form = BookEditForm(instance=instance)
    return render (request=request, template_name="library/forms/book_form.html", context={"form":form,"type":"edit","book":instance})

##### BOOK REFERENCES

def book_references(request):
    book_references = Book_Reference.objects.all()
    return render(request, 'library/book_references.html', {'book_references': book_references})

def book_reference(request, book_reference_id):
    book_reference = Book_Reference.objects.get(pk=book_reference_id)
    if book_reference is None:
        raise Http404("Book reference does not exist")
    return render(request, 'library/book_reference.html', {'book_reference': book_reference})

@librarian_required
def book_reference_create(request):
    if request.method == "POST":
        form = BookReferenceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Book reference created." )
            return redirect("library:book_references")
        messages.error(request, "Invalid form.")
    form = BookReferenceForm()
    return render (request=request, template_name="library/forms/book_reference_form.html", context={"form":form,"type":"create"})

@librarian_required
def book_reference_edit(request, book_reference_id):
    instance = Book_Reference.objects.get(pk=book_reference_id)
    if request.method == "POST":
        form = BookReferenceForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, "Book reference edited." )
            return redirect("library:book_references")
        messages.error(request, "Invalid form.")
    form = BookReferenceForm(instance=instance)
    return render (request=request, template_name="library/forms/book_reference_form.html", context={"form":form,"type":"edit","book":instance})

@librarian_required
def book_reference_delete(request, book_reference_id):
    book_reference = Book_Reference.objects.get(pk=book_reference_id)
    if book_reference is None:
        raise Http404("Book reference does not exist")
    book_reference.delete()
    messages.success(request, "Book reference deleted." )
    return redirect("library:book_references")

##### GENRES

def genres(request):
    genres = Genre.objects.all()
    return render(request, 'library/genres.html', {'genres': genres})
    
@librarian_required
def genre_create(request):
    if request.method == "POST":
        form = GenreForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Genre created." )
            return redirect("library:genres")
        messages.error(request, "Invalid form.")
    form = GenreForm()
    return render (request=request, template_name="library/forms/genre_form.html", context={"form":form,"type":"create"})

@librarian_required
def genre_update(request, genre_id):
    instance = Genre.objects.get(pk=genre_id)
    if request.method == "POST":
        form = GenreForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, "Genre edited." )
            return redirect("library:genres")
        messages.error(request, "Invalid form.")
    form = GenreForm(instance=instance)
    return render (request=request, template_name="library/forms/genre_form.html", context={"form":form,"type":"edit","genre":instance})

@librarian_required
def genre_delete(request, genre_id):
    genre = Genre.objects.get(pk=genre_id)
    if genre is None:
        raise Http404("Genre does not exist")
    genre.delete()
    messages.success(request, "Genre deleted." )
    return redirect("library:genres")