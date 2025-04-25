# accounts/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("profile/", views.UserProfileView.as_view(), name="my-profile"),
    path("profile/<int:pk>", views.UserProfileView.as_view(), name="user-profile"),
]