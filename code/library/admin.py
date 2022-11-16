from django.contrib import admin

# Register your models here.
from .models import Book, Library, Book_Reference, Genre

admin.site.register(Book)
admin.site.register(Book_Reference)
admin.site.register(Library)
admin.site.register(Genre)
