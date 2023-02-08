from django.urls import path

from . import views

app_name = 'library'
urlpatterns = [
    path('', views.index, name='home'),
    path('register', views.register, name='register'),
    path('register/member', views.register_member, name='register_member'),
    path('register/librarian', views.register_librarian, name='register_librarian'),
    path('books', views.books, name="books"),
    path('books/create', views.create_book, name="create_book"),
    path('books/<int:book_id>/edit', views.edit_book, name='edit_book'),
    path('books/<int:book_id>/', views.book_reference, name='book_reference'),
    path('books/<int:book_id>/borrow/', views.borrow_book, name='borrow_book'),
    #### BOOK REFERENCES
    path('book_references', views.book_references, name='book_references'),
    path('book_references/create', views.book_reference_create, name='book_reference_create'),
    path('book_references/<int:book_reference_id>/', views.book_reference, name='book_reference'),
    path('book_references/<int:book_reference_id>/edit', views.book_reference_edit, name='book_reference_edit'),
    path('book_references/<int:book_reference_id>/delete', views.book_reference_delete, name='book_reference_delete'),
    #### GENRES
    path('genres', views.genres, name='genres'),
    path('genres/create', views.genre_create, name='genre_create'),
    path('genres/<int:genre_id>/edit', views.genre_update, name='genre_update'),
    path('genres/<int:genre_id>/delete', views.genre_delete, name='genre_delete'),
]