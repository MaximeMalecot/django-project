from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ADMIN = 1
    LIBRARIAN = 2
    MEMBER = 3

    ROLE_CHOICES = (
        (ADMIN, 'admin'),
        (LIBRARIAN, 'librarian'),
        (MEMBER, 'member'),
    )
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, default=MEMBER)

class Library(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    zipcode = models.CharField(max_length=200)

    def __str__(self):
        return "{self.name} - {self.city}".format(self=self)

class Book_Reference(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    year = models.IntegerField()
    #cover = models.ImageField(upload_to='images/')
    edition = models.CharField(max_length=200)
    collection = models.CharField(max_length=200)
    synopsis = models.TextField()
    def __str__(self):
        return f"'{self.title}' by {self.author} ({self.year})"

class Book(models.Model):
    reference = models.ForeignKey(Book_Reference, on_delete=models.CASCADE)
    library = models.ForeignKey(Library, on_delete=models.CASCADE)
    stock = models.IntegerField(default=0)
    genre = models.ManyToManyField('Genre')
    def __str__(self):
        return f"{self.reference.__str__()} in {self.library.name}"

class Genre(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    def __str__(self):
        return self.name

# class Book_Genre(models.Model):
#     book = models.ForeignKey(Book, on_delete=models.CASCADE)
#     genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
#     def __str__(self):
#         return "{self.name} - {self.city}".format(self=self)