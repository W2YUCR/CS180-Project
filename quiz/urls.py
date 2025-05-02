from django.urls import path

from . import views

urlpatterns = [
    path("create/", views.QuizCreateView.as_view(), name="quiz-create"),
    path("<int:pk>/current", views.QuizCurrentView.as_view(), name="quiz-current"),
    path("<int:pk>/next", views.QuizNextView.as_view(), name="quiz-next"),
    path("<int:pk>/prev", views.QuizPrevView.as_view(), name="quiz-prev"),
    path("<int:pk>/", views.QuizView.as_view(), name="quiz-view"),
]
