from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator


class Author(models.Model):
    """Model representing a book author."""

    name = models.CharField(_("name"), max_length=255)
    biography = models.TextField(_("biography"), blank=True)
    birth_date = models.DateField(_("birth date"), null=True, blank=True)
    death_date = models.DateField(_("death date"), null=True, blank=True)
    photo = models.ImageField(_("photo"), upload_to="author_photos/", blank=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    class Meta:
        verbose_name = _("author")
        verbose_name_plural = _("authors")
        ordering = ["name"]

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Model representing a book genre."""

    name = models.CharField(_("name"), max_length=100, unique=True)
    description = models.TextField(_("description"), blank=True)

    class Meta:
        verbose_name = _("genre")
        verbose_name_plural = _("genres")

    def __str__(self):
        return self.name


class Book(models.Model):
    """Model representing a book."""

    title = models.CharField(_("title"), max_length=255)
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name="books", verbose_name=_("author")
    )
    genres = models.ManyToManyField(Genre, related_name="books")
    description = models.TextField(_("description"))
    cover_image = models.ImageField(
        _("cover image"), upload_to="book_covers/", blank=True
    )
    isbn = models.CharField(_("ISBN"), max_length=13, unique=True)
    publication_date = models.DateField(_("publication date"))
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    class Meta:
        verbose_name = _("book")
        verbose_name_plural = _("books")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} by {self.author.name}"

    @property
    def average_rating(self):
        return self.reviews.aggregate(models.Avg("rating"))["rating__avg"] or 0


class Review(models.Model):
    """Model representing a book review."""

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reviews"
    )
    rating = models.IntegerField(
        _("rating"), validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    title = models.CharField(_("title"), max_length=255)
    content = models.TextField(_("content"))
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    class Meta:
        verbose_name = _("review")
        verbose_name_plural = _("reviews")
        ordering = ["-created_at"]
        unique_together = ["book", "user"]

    def __str__(self):
        return f"Review of {self.book.title} by {self.user.username}"


class Comment(models.Model):
    """Model representing a comment on a review."""

    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name="comments"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments"
    )
    content = models.TextField(_("content"))
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    class Meta:
        verbose_name = _("comment")
        verbose_name_plural = _("comments")
        ordering = ["created_at"]

    def __str__(self):
        return f"Comment by {self.user.username} on {self.review}"
