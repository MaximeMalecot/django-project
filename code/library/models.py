from django.db import models

class Library(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    zipcode = models.CharField(max_length=200)

    def __str__(self):
        return self.name
class Book_Reference(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    year = models.IntegerField()
    #cover = models.ImageField(upload_to='images/')
    edition = models.CharField(max_length=200)
    collection = models.CharField(max_length=200)
    synopsis = models.TextField()

class Book(models.Model):
    reference = models.ForeignKey(Book_Reference, on_delete=models.CASCADE)
    library = models.ForeignKey(Library, on_delete=models.CASCADE)
    stock = models.IntegerField(default=0)

class Genre(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()

class Book_Genre(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)