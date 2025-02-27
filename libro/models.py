from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify

User = settings.AUTH_USER_MODEL


class Author(models.Model):
    """Model representing a book author. """

    name = models.CharField(_("name"), max_length=55)
    slug = models.SlugField(_("slug"), max_length=55, unique=True)
    biography = models.TextField(_("biography"), blank=True)
    birth_date = models.DateField(_("birth date"), null=True, blank=True)
    death_date = models.DateField(_("death date"), null=True, blank=True)
    photo = models.ImageField(_("photo"), upload_to="author_photos/", blank=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("author")
        verbose_name_plural = _("authors")
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("libro:author-detail", kwargs={"slug": self.slug})

    @property
    def book_count(self):
        return self.books.count()

    # Create a unique slug for each author
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            n = 1
            while Author.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{n}"
                n += 1
            self.slug = slug

        return super().save(*args, **kwargs)


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

    title = models.CharField(_("title"), max_length=200)
    slug = models.SlugField(_("slug"), max_length=205, unique=True)
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
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("book")
        verbose_name_plural = _("books")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} by {self.author.name}"

    @property
    def average_rating(self):
        return self.reviews.aggregate(models.Avg("rating"))["rating__avg"] or 0

    def get_absolute_url(self):
        return reverse("libro:book-detail", kwargs={"slug": self.slug})

    # Create a unique slug for each book
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            n = 1
            while Book.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{n}"
                n += 1
            self.slug = slug

        return super().save(*args, **kwargs)


class Review(models.Model):
    """Model representing a book review."""

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
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
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField(_("content"))
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    class Meta:
        verbose_name = _("comment")
        verbose_name_plural = _("comments")
        ordering = ["created_at"]

    def __str__(self):
        return f"Comment by {self.user.username} on {self.review}"
