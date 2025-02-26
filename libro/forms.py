from django import forms

from .models import Book, Review, Genre, Comment, Author


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = [
            "title",
            "author",
            "genres",
            "description",
            "cover_image",
            "isbn",
            "publication_date",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "author": forms.Select(attrs={"class": "form-control"}),
            "genres": forms.CheckboxSelectMultiple(),
            "description": forms.Textarea(attrs={"class": "form-control"}),
            "cover_image": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "isbn": forms.TextInput(attrs={"class": "form-control"}),
            "publication_date": forms.DateInput(attrs={"class": "form-control"}),
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "content"]
        widgets = {
            "rating": forms.NumberInput(
                attrs={"class": "form-control", "min": 1, "max": 5}
            ),
            "content": forms.Textarea(attrs={"class": "form-control"}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(attrs={"class": "form-control"}),
        }


class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
        }


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ["name", "biography", "birth_date", "death_date", "photo"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "biography": forms.Textarea(attrs={"class": "form-control"}),
            "birth_date": forms.DateInput(attrs={"class": "form-control"}),
            "death_date": forms.DateInput(attrs={"class": "form-control"}),
            "photo": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }
