from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth import login
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _

from .forms import CustomUserCreationForm


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
