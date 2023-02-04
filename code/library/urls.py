from django.urls import path

from . import views

app_name = 'library'
urlpatterns = [
    path('', views.index, name='books'),
    path('<int:book_id>/', views.book_reference, name='book_reference')
]