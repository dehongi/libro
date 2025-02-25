from django.urls import path
from .views import (
    AuthorListView,
    AuthorDetailView,
    AuthorCreateView,
    AuthorUpdateView,
    AuthorDeleteView,
    BookListView,
    BookDetailView,
    BookCreateView,
    BookUpdateView,
    BookDeleteView,
)

app_name = "libro"

urlpatterns = [
    path("authors/", AuthorListView.as_view(), name="author-list"),
    path("authors/<int:pk>/", AuthorDetailView.as_view(), name="author-detail"),
    path("authors/add/", AuthorCreateView.as_view(), name="author-create"),
    path("authors/<int:pk>/edit/", AuthorUpdateView.as_view(), name="author-update"),
    path("authors/<int:pk>/delete/", AuthorDeleteView.as_view(), name="author-delete"),
    path("books/", BookListView.as_view(), name="book-list"),
    path("books/<int:pk>/", BookDetailView.as_view(), name="book-detail"),
    path("books/add/", BookCreateView.as_view(), name="book-create"),
    path("books/<int:pk>/edit/", BookUpdateView.as_view(), name="book-update"),
    path("books/<int:pk>/delete/", BookDeleteView.as_view(), name="book-delete"),
]
