from django.urls import path

from . import views

urlpatterns = [
    path('', views.DeckListView.as_view()),
    path("<int:pk>", views.DeckDetailView.as_view(), name='deck-detail'),
    path("create/", views.DeckCreateView.as_view(), name='deck-create')
]