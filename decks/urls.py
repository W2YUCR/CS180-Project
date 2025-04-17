from django.urls import path

from . import views

urlpatterns = [
    path('', views.DeckListView.as_view(), name='decks'),
    path("<int:pk>", views.DeckDetailView.as_view(), name='deck-detail'),
    path("create/", views.DeckCreateView.as_view(), name='deck-create'),
    path('<int:deck_pk>/create', views.CardCreateView.as_view(), name='card-create'),
    path('cards/<int:pk>', views.CardDetailView.as_view(), name='card-detail'),
    path('cards/<int:pk>/update', views.CardUpdateView.as_view(), name='card-update'),
    path('cards/<int:pk>/delete', views.CardDeleteView.as_view(), name='card-delete'),
]