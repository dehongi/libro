from django.urls import path
from .views import (
    SignupView,
    ProfileView,
    PublicProfileView,
    ProfileEditView,
    CustomPasswordChangeView,
)

urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("profile/edit/", ProfileEditView.as_view(), name="profile-edit"),
    path(
        "profile/change-password/",
        CustomPasswordChangeView.as_view(),
        name="change-password",
    ),
    path("users/<str:username>/", PublicProfileView.as_view(), name="public-profile"),
]
