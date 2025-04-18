from django.urls import path

from . import views

urlpatterns = [
    path("<int:pk>/", views.QuizView.as_view(), name="quiz-view"),
    path("create/", views.QuizCreateView.as_view(), name="quiz-create"),
    path("<int:pk>/current", views.QuizCurrentView.as_view(), name="quiz-current"),
    path("<int:pk>/next", views.QuizNextView.as_view(), name="quiz-next"),
]
