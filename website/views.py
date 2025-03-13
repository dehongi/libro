from django.shortcuts import render
from django.views.generic import TemplateView
from django.utils.translation import gettext_lazy as _

from libro.models import Book

# Create your views here.


class HomeView(TemplateView):
    """Home page of the website."""

    template_name = "website/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["latest_books"] = Book.objects.all().order_by("-created_at")[:3]
        context["title"] = _("Welcome to Libro")
        return context


class AboutView(TemplateView):
    """About page."""

    template_name = "website/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("About Us")
        return context


class ContactView(TemplateView):
    """Contact page."""

    template_name = "website/contact.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Contact Us")
        return context


class TermsView(TemplateView):
    """Terms of service page."""

    template_name = "website/terms.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Terms of Service")
        return context


class PrivacyView(TemplateView):
    """Privacy policy page."""

    template_name = "website/privacy.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Privacy Policy")
        return context
