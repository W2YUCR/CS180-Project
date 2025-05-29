from django.urls import path

from . import views

urlpatterns = [
    path("<int:deck_pk>", views.ReviewView.as_view(), name="review"),
]
