from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView
from django.contrib.auth import login
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.contrib import messages
from django.utils.translation import gettext_lazy as _

from .forms import CustomUserCreationForm
from .models import CustomUser


class SignupView(SuccessMessageMixin, CreateView):
    """View for user registration."""

    form_class = CustomUserCreationForm
    template_name = "accounts/signup.html"
    success_url = reverse_lazy("website:home")
    success_message = _("Welcome! Your account has been created successfully.")

    def form_valid(self, form):
        """Log the user in after successful registration."""
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


class ProfileView(LoginRequiredMixin, DetailView):
    """Private profile view for logged-in user."""

    model = CustomUser
    template_name = "accounts/profile.html"
    context_object_name = "profile"

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context.update(
            {
                "reviews_count": user.reviews.count(),
                "comments_count": user.comments.count(),
                "latest_reviews": user.reviews.select_related("book").order_by(
                    "-created_at"
                )[:5],
                "latest_comments": user.comments.select_related(
                    "review", "review__book"
                ).order_by("-created_at")[:5],
            }
        )
        return context


class PublicProfileView(DetailView):
    """Public profile view accessible by username."""

    model = CustomUser
    template_name = "accounts/public_profile.html"
    context_object_name = "profile"
    slug_field = "username"
    slug_url_kwarg = "username"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        context.update(
            {
                "reviews_count": user.reviews.count(),
                "comments_count": user.comments.count(),
                "latest_reviews": user.reviews.select_related("book").order_by(
                    "-created_at"
                )[:5],
                "latest_comments": user.comments.select_related(
                    "review", "review__book"
                ).order_by("-created_at")[:5],
            }
        )
        return context


class ProfileEditView(LoginRequiredMixin, UpdateView):
    """View for editing user profile."""

    model = CustomUser
    template_name = "accounts/profile_edit.html"
    fields = [
        "first_name",
        "last_name",
        "email",
        "phone_number",
        "date_of_birth",
        "address",
    ]
    success_url = reverse_lazy("accounts:profile")

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, _("Your profile has been updated successfully."))
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Edit Profile")
        return context


class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    """Custom view for changing password."""

    template_name = "accounts/password_change.html"
    success_url = reverse_lazy("accounts:profile")

    def form_valid(self, form):
        messages.success(
            self.request, _("Your password has been changed successfully.")
        )
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Change Password")
        return context
