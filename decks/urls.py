from django.urls import path

from . import views

urlpatterns = [
    path("", views.DeckListView.as_view(), name="decks"),
    path("<int:pk>/", views.DeckDetailView.as_view(), name="deck-detail"),  # add slash here
    path("create/", views.DeckCreateView.as_view(), name="deck-create"),
    path("<int:pk>/update/", views.DeckUpdateView.as_view(), name="deck-update"),  # slash here
    path("<int:pk>/delete/", views.DeckDeleteView.as_view(), name="deck-delete"),  # slash here
    path("<int:deck_pk>/cards/create/", views.CardCreateView.as_view(), name="card-create"),
    path("cards/<int:pk>/", views.CardDetailView.as_view(), name="card-detail"),  # slash here
    path("cards/<int:pk>/update/", views.CardUpdateView.as_view(), name="card-update"),  # slash here
    path("cards/<int:pk>/delete/", views.CardDeleteView.as_view(), name="card-delete"),  # slash here
    path("shared/", views.SharedDecksView.as_view(), name="shared-decks"),
]
