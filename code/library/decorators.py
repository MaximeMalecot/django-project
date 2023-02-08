from django.contrib import messages
from django.shortcuts import  redirect
from .models import User

default_message = "You don't have permission to access this page."

def librarian_required(function=None):
    def _function(request,*args,**kwargs):
        if hasattr(request.user, "role") and request.user.role == User.LIBRARIAN:
            if hasattr(request.user, "library") and request.user.library != None:
                return function(request,*args,**kwargs)
            else :
                messages.error(request, "You don't have a library assigned.")
                return redirect('library:home')
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