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
    
    
class CreateBookReferenceForm(forms.ModelForm):
    genre = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all()
    )
    
    class Meta:
        model = Book_Reference
        fields = ('title', 'author', 'year', 'edition', 'collection', 'synopsis', 'genre')
    
    def __init__(self, *args, **kwargs):
        super(CreateBookReferenceForm, self).__init__(*args, **kwargs)
        self.fields['genre'].required = False
    
    def save(self, commit=True):
        instance = super(CreateBookReferenceForm, self).save(commit=False)
        if commit:
            instance.save()
        return instance