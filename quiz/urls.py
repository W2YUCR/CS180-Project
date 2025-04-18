from django.urls import path

from . import views

urlpatterns = [
    path("<int:pk>/", views.QuizView.as_view(), name="quiz-view"),
    path("create/", views.QuizCreateView.as_view(), name="quiz-create"),
]
