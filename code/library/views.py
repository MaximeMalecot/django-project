from django.http import HttpResponse, Http404
from django.shortcuts import  render, redirect
from .models import Book, Book_Reference, Genre, User, Library, Loan
from .forms import RegisterUserForm, RegisterLibrarianForm, BookReferenceForm, BookForm, BookEditForm, GenreForm, BookAddByRefForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .decorators import librarian_required, admin_required
import datetime

# Default views

def index(request):
    search = None
    if request.method == "POST":
        if request.POST.get('search') != "":
            search = request.POST.get('search')
    if search is not None:
        books = Book_Reference.objects.filter(title__icontains=search)
    else :
        books = Book_Reference.objects.all()
    if request.user.is_authenticated:
        if request.user.role == User.MEMBER:
            return render(request, 'library/index_member.html', {'books': books})
        if request.user.role == User.LIBRARIAN:
            return render(request, 'library/index_librarian.html', {'books': books})
    return render(request, 'library/books.html', {'books': books})

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

##### BOOKS

def books_by_ref(request, ref_id):
    book = Book_Reference.objects.get(pk=ref_id)
    add_book = False
    if request.user.is_authenticated:
        if request.user.role == User.LIBRARIAN and request.user.library is not None:
            book_exists = Book.objects.filter(reference=ref_id, library=request.user.library).exists()
            add_book = not book_exists
    if book is None:
        raise Http404("Book reference does not exist")
    availabilities = Book.objects.filter(reference=book, stock__gt=0)
    return render(request, 'library/book.html', {'book': book, 'availabilities': availabilities, 'add_book': add_book})

def books_by_library_by_ref(request, library_id, ref_id):
    book = Book.objects.get(reference=ref_id, library=library_id)
    return render(request, 'library/book_in_library.html', {'book': book})

def books_by_genre(request, genre_id):
    books = Book_Reference.objects.filter(genre=genre_id)
    return render(request, 'library/index.html', {'books': books})

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
def book_edit(request, book_id):
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

@librarian_required
def book_delete(request, book_id):
    book = Book.objects.get(pk=book_id)
    if book is None:
        raise Http404("Book does not exist")
    book.delete()
    messages.success(request, "Book deleted.")
    return redirect("library:home")
    
##### BOOK REFERENCES

def book_references(request):
    book_references = Book_Reference.objects.all()
    return render(request, 'library/book_references.html', {'book_references': book_references})

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
def book_reference_add_book(request, book_reference_id):
    book_ref = Book_Reference.objects.get(pk=book_reference_id)
    library = request.user.library
    book_exists = Book.objects.filter(reference=book_ref, library=library).exists()
    if book_exists == True:
        messages.error(request, "Book already exists in your library." )
        return redirect("library:home")
        
    if request.method == "POST":
        form = BookAddByRefForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.reference = book_ref
            book.library = library
            book.save()
            messages.success(request, "Book created." )
            return redirect("library:home")
        messages.error(request, "Invalid form.")
    form = BookAddByRefForm(initial={'reference': book_ref.id, 'library': library.id})
    return render (request=request, template_name="library/forms/book_reference_add_form.html", context={"form":form})


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


##### LIBRARIES
def libraries(request): ### ALL LIBRARIES
    libraries = Library.objects.all()
    return render(request, 'library/libraries.html', {'libraries': libraries})

def library(request, library_id):### ALL BOOKS FROM LIBRARY
    library = Library.objects.get(pk=library_id)
    books = Book.objects.filter(library=library)
    if library is None:
        raise Http404("Library does not exist")
    return render(request, 'library/library.html', {'library': library,'books':books})

##### LOANS

@login_required
def own_loans(request):
    loans = Loan.objects.get(borrower=request.user)
    return render(request, 'library/loans.html', {'loans': loans})

@login_required
def borrow_book(request, book_id):
    book = Book.objects.get(pk=book_id)
    if book is None:
        messages.error(request, "Book does not exist")
        return redirect("library:home")
    if book.stock <= 0:
        messages.error(request, "Book is not available")
        return redirect("library:home")
    loan_exists = Loan.objects.filter(book=book, borrower=request.user, isActive=True).exists()
    if loan_exists == True:
        messages.error(request, "You already have loaned this book, return it before borrowing it")
        return redirect("library:home")
    book.stock = book.stock - 1
    book.save()
    loan = Loan(book=book, borrower=request.user, dueDate=timezone.now() + datetime.timedelta(days=30))
    loan.save()
    return render(request, 'library/borrowed.html', {'book': book})

@librarian_required
def loans(request):
    isActive = request.GET.get('isActive', None)
    if isActive != None:
        loans = Loan.objects.filter(book__library=request.user.library.id, isActive=isActive)
    else :
        loans = Loan.objects.filter(book__library=request.user.library.id)
    return render(request, 'library/loans.html', {'loans': loans})

@librarian_required
def user_loans(request, user_id):
    user = User.objects.get(pk=user_id)
    if user is None:
        messages.error(request, "User does not exist")
        return redirect("library:loans")
    loans = Loan.objects.filter(book__library=request.user.library.id, borrower=user)
    return render(request, 'library/user_loans.html', {'user': user, 'loans': loans})

@librarian_required
def return_book(request, loan_id):
    loan = Loan.objects.get(pk=loan_id)
    if loan is None:
        messages.error(request, "Loan does not exist")
        return redirect("library:loans")
    if loan.book.library != request.user.library:
        messages.error(request, "You can't return a book from another library")
        return redirect("library:loans")
    if loan.isActive == False:
        messages.error(request, "Book is already returned")
        return redirect("library:loans")
    loan.isActive = False
    loan.save()
    book = loan.book
    book.stock = book.stock + 1
    book.save()
    messages.success(request, "Book returned")
    return redirect("library:loans")