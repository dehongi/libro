from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
    FormView,
)
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.exceptions import ValidationError
from django.core.files.storage import default_storage
import json
from django.core.files.base import ContentFile
from django.template.defaultfilters import slugify
import requests

from .models import Author, Book, Review, Comment
from .forms import (
    AuthorForm,
    BookForm,
    ReviewForm,
    CommentForm,
    AuthorBatchUploadForm,
    BookBatchUploadForm,
)
from .utils import process_book_cover, process_author_photo


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

    def form_valid(self, form):
        if form.instance.photo:
            form.instance.photo = process_author_photo(form.instance.photo)
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Add Author")
        return context


class AuthorUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Update an existing author."""

    model = Author
    template_name = "libro/author_form.html"
    form_class = AuthorForm

    def form_valid(self, form):
        if form.instance.photo:
            form.instance.photo = process_author_photo(form.instance.photo)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Edit Author")
        return context

    def test_func(self):
        author = self.get_object()
        return self.request.user == author.created_by


class AuthorDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Delete an author."""

    model = Author
    template_name = "libro/author_confirm_delete.html"
    success_url = reverse_lazy("author-list")
    context_object_name = "author"

    def test_func(self):
        author = self.get_object()
        return self.request.user == author.created_by

    def get_success_url(self):
        return reverse_lazy("libro:author-list")


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

    def dispatch(self, request, *args, **kwargs):
        self.author = get_object_or_404(Author, slug=self.kwargs["author_slug"])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        if form.instance.cover_image:
            form.instance.cover_image = process_book_cover(form.instance.cover_image)
        form.instance.author = self.author
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Add Book")
        return context


class BookUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Update an existing book."""

    model = Book
    form_class = BookForm
    template_name = "libro/book_form.html"

    def form_valid(self, form):
        if form.instance.cover_image:
            form.instance.cover_image = process_book_cover(form.instance.cover_image)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Edit Book")
        return context

    def test_func(self):
        book = self.get_object()
        return self.request.user == book.created_by


class BookDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Delete a book."""

    model = Book
    template_name = "libro/book_confirm_delete.html"
    success_url = reverse_lazy("libro:book-list")
    context_object_name = "book"

    def test_func(self):
        book = self.get_object()
        return self.request.user == book.created_by

    def get_success_url(self):
        return reverse_lazy("libro:book-list")


class LibroHome(TemplateView):
    """Home page for the libro app showing latest books and authors."""

    template_name = "libro/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Explore Books & Authors")
        context["latest_books"] = Book.objects.all().order_by("-created_at")[:6]
        context["featured_authors"] = Author.objects.all().order_by("?")[:3]
        return context


@login_required
@require_POST
def add_review(request, book_slug):
    """Add a review to a book."""
    book = get_object_or_404(Book, slug=book_slug)
    form = ReviewForm(request.POST)

    try:
        # Check if user has already reviewed this book
        if Review.objects.filter(book=book, user=request.user).exists():
            messages.error(request, _("You have already reviewed this book."))
            return redirect(
                "libro:book-detail", author_slug=book.author.slug, slug=book_slug
            )

        if form.is_valid():
            review = form.save(commit=False)
            review.book = book
            review.user = request.user
            review.save()
            messages.success(request, _("Your review has been added successfully."))
        else:
            messages.error(request, _("Please correct the errors below."))
    except ValidationError as e:
        messages.error(request, str(e))

    return redirect("libro:book-detail", author_slug=book.author.slug, slug=book_slug)


@login_required
@require_POST
def edit_review(request, review_id):
    """Edit an existing review."""
    review = get_object_or_404(Review, id=review_id, user=request.user)
    form = ReviewForm(request.POST, instance=review)

    if form.is_valid():
        form.save()
        messages.success(request, _("Your review has been updated successfully."))
    else:
        messages.error(request, _("Please correct the errors below."))

    return redirect(
        "libro:book-detail",
        author_slug=review.book.author.slug,
        book_slug=review.book.slug,
    )


@login_required
@require_POST
def delete_review(request, review_id):
    """Delete a review."""
    review = get_object_or_404(Review, id=review_id, user=request.user)
    book = review.book
    review.delete()
    messages.success(request, _("Your review has been deleted successfully."))
    return redirect(
        "libro:book-detail", author_slug=book.author.slug, book_slug=book.slug
    )


@login_required
@require_POST
def add_comment(request, review_id):
    """Add a comment to a review."""
    review = get_object_or_404(Review, id=review_id)
    form = CommentForm(request.POST)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.review = review
        comment.user = request.user
        comment.save()

        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse(
                {
                    "status": "success",
                    "comment": {
                        "content": comment.content,
                        "user": comment.user.username,
                        "created_at": comment.created_at.strftime("%B %d, %Y"),
                    },
                }
            )

        messages.success(request, _("Your comment has been added successfully."))
    else:
        messages.error(request, _("Please enter a valid comment."))

    return redirect(
        "libro:book-detail",
        author_slug=review.book.author.slug,
        slug=review.book.slug,
    )


@login_required
@require_POST
def delete_comment(request, comment_id):
    """Delete a comment."""
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)
    book = comment.review.book
    comment.delete()

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return JsonResponse({"status": "success"})

    messages.success(request, _("Your comment has been deleted successfully."))
    return redirect(
        "libro:book-detail", author_slug=book.author.slug, book_slug=book.slug
    )


class AuthorBatchUploadView(LoginRequiredMixin, FormView):
    """Upload multiple authors from a JSON file."""

    template_name = "libro/author_batch_upload.html"
    form_class = AuthorBatchUploadForm
    success_url = reverse_lazy("libro:author-list")

    def form_valid(self, form):
        json_file = form.cleaned_data["file"]

        try:
            data = json.load(json_file)
            created_count = 0
            skipped_count = 0

            for author_data in data:
                name = author_data.get("name")
                if not name:
                    continue

                # Check if author already exists
                if Author.objects.filter(name=name).exists():
                    skipped_count += 1
                    continue

                # Create new author
                author = Author(
                    name=name,
                    biography=author_data.get("biography", ""),
                    birth_date=author_data.get("birth_date"),
                    death_date=author_data.get("death_date"),
                    created_by=self.request.user,
                )

                # Handle photo if provided as URL
                photo_url = author_data.get("photo")
                if photo_url:
                    try:
                        response = requests.get(photo_url)
                        if response.status_code == 200:
                            file_name = f"author_photos/{slugify(name)}.jpg"
                            default_storage.save(
                                file_name, ContentFile(response.content)
                            )
                            author.photo = file_name
                    except:
                        pass

                author.save()
                created_count += 1

            messages.success(
                self.request,
                _(
                    "Successfully created %(created)d authors. %(skipped)d duplicates skipped."
                )
                % {"created": created_count, "skipped": skipped_count},
            )

        except json.JSONDecodeError:
            messages.error(self.request, _("Invalid JSON file format."))
        except Exception as e:
            messages.error(
                self.request,
                _("An error occurred while processing the file: %(error)s")
                % {"error": str(e)},
            )

        return super().form_valid(form)


class BookBatchUploadView(LoginRequiredMixin, FormView):
    """Upload multiple books from a JSON file."""

    template_name = "libro/book_batch_upload.html"
    form_class = BookBatchUploadForm

    def dispatch(self, request, *args, **kwargs):
        self.author = get_object_or_404(Author, slug=self.kwargs["author_slug"])
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("libro:author-books", kwargs={"author_slug": self.author.slug})

    def form_valid(self, form):
        json_file = form.cleaned_data["file"]

        try:
            data = json.load(json_file)
            created_count = 0
            skipped_count = 0

            for book_data in data:
                title = book_data.get("title")
                if not title:
                    continue

                # Check if book already exists for this author
                if Book.objects.filter(author=self.author, title=title).exists():
                    skipped_count += 1
                    continue

                # Create new book
                book = Book(
                    title=title,
                    description=book_data.get("description", ""),
                    isbn=book_data.get("isbn", ""),
                    publication_date=book_data.get("publication_date"),
                    author=self.author,
                    created_by=self.request.user,
                )

                # Handle cover image if provided as URL
                cover_url = book_data.get("cover_image")
                if cover_url:
                    try:
                        response = requests.get(cover_url)
                        if response.status_code == 200:
                            file_name = f"book_covers/{slugify(title)}.jpg"
                            default_storage.save(
                                file_name, ContentFile(response.content)
                            )
                            book.cover_image = file_name
                    except:
                        pass

                book.save()
                created_count += 1

            messages.success(
                self.request,
                _(
                    "Successfully created %(created)d books. %(skipped)d duplicates skipped."
                )
                % {"created": created_count, "skipped": skipped_count},
            )

        except json.JSONDecodeError:
            messages.error(self.request, _("Invalid JSON file format."))
        except Exception as e:
            messages.error(
                self.request,
                _("An error occurred while processing the file: %(error)s")
                % {"error": str(e)},
            )

        return super().form_valid(form)
