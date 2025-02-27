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
    AuthorBookListView,
    LibroHome,
    add_review,
    edit_review,
    delete_review,
    add_comment,
    delete_comment,
)

app_name = "libro"

urlpatterns = [
    path("", LibroHome.as_view(), name="home"),
    path("authors/", AuthorListView.as_view(), name="author-list"),
    path("authors/add/", AuthorCreateView.as_view(), name="author-create"),
    path("authors/<slug:slug>/", AuthorDetailView.as_view(), name="author-detail"),
    path("authors/<slug:slug>/edit/", AuthorUpdateView.as_view(), name="author-update"),
    path(
        "authors/<slug:slug>/delete/", AuthorDeleteView.as_view(), name="author-delete"
    ),
    path(
        "authors/<slug:author_slug>/books/",
        AuthorBookListView.as_view(),
        name="author-books",
    ),
    path("books/", BookListView.as_view(), name="book-list"),
    path(
        "authors/<slug:author_slug>/books/add/",
        BookCreateView.as_view(),
        name="book-create",
    ),
    path(
        "authors/<slug:author_slug>/books/<slug:slug>/",
        BookDetailView.as_view(),
        name="book-detail",
    ),
    path(
        "authors/<slug:author_slug>/books/<slug:slug>/edit/",
        BookUpdateView.as_view(),
        name="book-update",
    ),
    path(
        "authors/<slug:author_slug>/books/<slug:slug>/delete/",
        BookDeleteView.as_view(),
        name="book-delete",
    ),
    path("books/<slug:book_slug>/review/add/", add_review, name="add-review"),
    path("reviews/<int:review_id>/edit/", edit_review, name="edit-review"),
    path("reviews/<int:review_id>/delete/", delete_review, name="delete-review"),
    path("reviews/<int:review_id>/comment/add/", add_comment, name="add-comment"),
    path("comments/<int:comment_id>/delete/", delete_comment, name="delete-comment"),
]
