from django.urls import path

from . import views

app_name = 'library'
urlpatterns = [
    path('', views.index, name='home'),
    path('register', views.register, name='register'),
    path('register/member', views.register_member, name='register_member'),
    path('register/librarian', views.register_librarian, name='register_librarian'),
    
    #### BOOKS
    path('books/create', views.create_book, name="create_book"),
    path('books/<int:ref_id>', views.books_by_ref, name='books_by_ref'),
    path('books/<int:book_id>/edit', views.book_edit, name='book_edit'),
    path('books/<int:book_id>/delete', views.book_delete, name='book_delete'),
    path('books/<int:book_id>/borrow/', views.borrow_book, name='borrow_book'),
    path('books/<int:library_id>/<int:ref_id>', views.books_by_library_by_ref, name='books_by_library_by_ref'),
    
    #### BOOK REFERENCES
    path('book_references', views.book_references, name='book_references'),
    path('book_references/create', views.book_reference_create, name='book_reference_create'),
    path('book_references/<int:book_reference_id>/edit', views.book_reference_edit, name='book_reference_edit'),
    path('book_references/<int:book_reference_id>/delete', views.book_reference_delete, name='book_reference_delete'),
    #### GENRES
    path('genres', views.genres, name='genres'),
    path('genres/create', views.genre_create, name='genre_create'),
    path('genres/<int:genre_id>/edit', views.genre_update, name='genre_update'),
    path('genres/<int:genre_id>/delete', views.genre_delete, name='genre_delete'),
    path('genres/<int:genre_id>', views.books_by_genre, name='genre_books'),
    
    #### LIBRARY
    path('libraries', views.libraries, name='libraries'),
    path('libraries/<int:library_id>', views.library, name='library'), ### AFFICHE LES LIVRES D'UNE BIBLIOTHEQUE
]