from django.shortcuts import render
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils.translation import gettext_lazy as _

from .models import Author
from .forms import AuthorForm


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
