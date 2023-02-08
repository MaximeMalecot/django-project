from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Library, Book_Reference, Book, Genre


class RegisterUserForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(RegisterUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user

class RegisterLibrarianForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        
    def save(self, commit=True):
        user = super(RegisterLibrarianForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.role = User.LIBRARIAN
        if commit: 
            user.save()
        return user
    
    
class BookReferenceForm(forms.ModelForm):
    genre = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all()
    )
    
    class Meta:
        model = Book_Reference
        fields = ('title', 'author', 'year', 'edition', 'collection', 'synopsis', 'genre')
    
    def __init__(self, *args, **kwargs):
        super(BookReferenceForm, self).__init__(*args, **kwargs)
        self.fields['genre'].required = False
    
    def save(self, commit=True):
        instance = super(BookReferenceForm, self).save(commit=False)
        if commit:
            instance.save()
        return instance

class BookForm(forms.ModelForm):
    reference = forms.ModelChoiceField(
        queryset=Book_Reference.objects.all()
    )
    stock = forms.IntegerField()
    
    class Meta:
        model = Book
        fields = ('reference', 'stock')
        
    def save(self, commit=True):
        instance = super(BookForm, self).save(commit=False)
        if commit:
            instance.save()
        return instance
    
class BookEditForm(forms.ModelForm):
    reference = forms.ModelChoiceField(
        queryset=Book_Reference.objects.all(),
        disabled=True
    )
    stock = forms.IntegerField()
    
    class Meta:
        model = Book
        fields = ('reference', 'stock')
        
    def save(self, commit=True):
        instance = super(BookEditForm, self).save(commit=False)
        if commit:
            instance.save()
        return instance
    
class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ('name', 'description')
        
    def save(self, commit=True):
        instance = super(GenreForm, self).save(commit=False)
        if commit:
            instance.save()
        return instance