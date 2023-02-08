from django.db import models
from django.contrib.auth.models import AbstractUser

class Library(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    zipcode = models.CharField(max_length=200)

    def __str__(self):
        return "{self.name} - {self.city}".format(self=self)
    
class User(AbstractUser):
    library = models.ForeignKey(Library, on_delete=models.CASCADE, blank=True, null=True)
    
    ADMIN = 1
    LIBRARIAN = 2
    MEMBER = 3

    ROLE_CHOICES = (
        (ADMIN, 'admin'),
        (LIBRARIAN, 'librarian'),
        (MEMBER, 'member'),
    )
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, default=MEMBER)

class Genre(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
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
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, blank=True, null=True)
    def __str__(self):
        return f"'{self.title}' by {self.author} ({self.year})"

class Book(models.Model):
    reference = models.ForeignKey(Book_Reference, on_delete=models.CASCADE)
    library = models.ForeignKey(Library, on_delete=models.CASCADE)
    stock = models.IntegerField(default=0)
    def __str__(self):
        return f"{self.reference.__str__()} in {self.library.name}"

class Topic(models.Model):
    title = models.CharField(max_length=200)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.title

class Message(models.Model):
    content = models.TextField()
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    deletedAt = models.DateTimeField(null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.author.username} wrote on {self.topic.title} : {self.content[:20]}..."
    
class Loan(models.Model):
    createdAt = models.DateTimeField(auto_now_add=True)
    dueDate = models.DateTimeField()
    borrower = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.borrower.username} borrowed {self.book.reference.title} on {self.createdAt}"
    
class Reading_Group(models.Model):
    title = models.CharField(max_length=200)
    meetingDate = models.DateTimeField()
    library = models.ForeignKey(Library, on_delete=models.CASCADE)
    participants = models.ManyToManyField(User)
    def __str__(self):
        return f"{self.title} on {self.meetingDate}"