from django.urls import path

from . import views

app_name = 'library'

urlpatterns = [
    path('', views.BookListView.as_view(), name='book_list'),
    path('books/new/', views.BookCreateView.as_view(), name='book_create'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book_detail'),
    path('books/<int:pk>/edit/', views.BookUpdateView.as_view(), name='book_update'),
    path('books/<int:pk>/delete/', views.BookDeleteView.as_view(), name='book_delete'),
    path('authors/', views.AuthorListView.as_view(), name='author_list'),
    path('authors/<int:pk>/', views.AuthorDetailView.as_view(), name='author_detail'),
]
