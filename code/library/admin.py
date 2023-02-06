from django.contrib import admin

# Register your models here.
from .models import Book, Library, Book_Reference, Genre, User

admin.site.register(User)
admin.site.register(Book)
admin.site.register(Book_Reference)
admin.site.register(Library)
admin.site.register(Genre)
