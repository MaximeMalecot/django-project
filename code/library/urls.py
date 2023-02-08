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
    path('books/<int:book_id>/', views.book_reference, name='book_reference'),
    path('books/<int:book_id>/borrow/', views.borrow_book, name='borrow_book'),
    path('book_references/create', views.create_book_reference, name='create_book_reference'),
    path('book_references/<int:book_reference_id>/edit', views.edit_book_reference, name='edit_book_reference'),
]