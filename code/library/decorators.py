from django.contrib import messages
from django.shortcuts import  redirect
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from .models import User

default_message = "You don't have permission to access this page."

def librarian_required(function=None):
    def _function(request,*args,**kwargs):
        if hasattr(request.user, "role") and request.user.role == User.LIBRARIAN:
            return function(request,*args,**kwargs)
        else:
            messages.error(request, default_message)
            return redirect('library:home')
    return _function


def admin_required(function=None):
    def _function(request,*args,**kwargs):
        if hasattr(request.user, "role") and request.user.role == User.ADMIN:
            return function(request,*args,**kwargs)
        else:
            messages.error(request, default_message)
            return redirect('library:home')
    return _function