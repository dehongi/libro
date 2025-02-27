from django.shortcuts import render
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
)
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils.translation import gettext_lazy as _

from .models import Author, Book
from .forms import AuthorForm, BookForm


class AuthorListView(ListView):
    """Display a list of all authors."""

    model = Author
    context_object_name = "authors"
    template_name = "libro/author_list.html"
    paginate_by = 10


class AuthorDetailView(DetailView):
    """Display detailed information about an author."""

    model = Author
    context_object_name = "author"
    template_name = "libro/author_detail.html"


class AuthorCreateView(LoginRequiredMixin, CreateView):
    """Create a new author."""

    model = Author
    template_name = "libro/author_form.html"
    form_class = AuthorForm
    success_url = reverse_lazy("libro:author-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Add Author")
        return context


class AuthorUpdateView(LoginRequiredMixin, UpdateView):
    """Update an existing author."""

    model = Author
    template_name = "libro/author_form.html"
    form_class = AuthorForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Edit Author")
        return context

    def get_success_url(self):
        return reverse_lazy("libro:author-detail", kwargs={"pk": self.object.pk})


class AuthorDeleteView(LoginRequiredMixin, DeleteView):
    """Delete an author."""

    model = Author
    template_name = "libro/author_confirm_delete.html"
    success_url = reverse_lazy("author-list")
    context_object_name = "author"


class AuthorBookListView(ListView):
    """Display a list of books written by an author."""

    model = Book
    template_name = "libro/author_book_list.html"
    context_object_name = "books"
    paginate_by = 10

    def get_queryset(self):
        author = Author.objects.get(slug=self.kwargs["author_slug"])
        return Book.objects.filter(author=author)


class BookListView(ListView):
    """Display a list of all books."""

    model = Book
    context_object_name = "books"
    template_name = "libro/book_list.html"
    paginate_by = 12


class BookDetailView(DetailView):
    """Display detailed information about a book."""

    model = Book
    context_object_name = "book"
    template_name = "libro/book_detail.html"


class BookCreateView(LoginRequiredMixin, CreateView):
    """Create a new book."""

    model = Book
    form_class = BookForm
    template_name = "libro/book_form.html"
    success_url = reverse_lazy("libro:book-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Add Book")
        return context


class BookUpdateView(LoginRequiredMixin, UpdateView):
    """Update an existing book."""

    model = Book
    form_class = BookForm
    template_name = "libro/book_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Edit Book")
        return context

    def get_success_url(self):
        return reverse_lazy("libro:book-detail", kwargs={"pk": self.object.pk})


class BookDeleteView(LoginRequiredMixin, DeleteView):
    """Delete a book."""

    model = Book
    template_name = "libro/book_confirm_delete.html"
    success_url = reverse_lazy("libro:book-list")
    context_object_name = "book"


class LibroHome(TemplateView):
    """Home page for the libro app showing latest books and authors."""

    template_name = "libro/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Explore Books & Authors")
        context["latest_books"] = Book.objects.all().order_by("-created_at")[:6]
        context["featured_authors"] = Author.objects.all().order_by("?")[:3]
        return context
