from django.urls import reverse_lazy
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import MultipleObjectMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from decks.models import Card, Deck
from typing import override

class DeckListView(LoginRequiredMixin, ListView):
    context_object_name='deck_list'
    @override
    def get_queryset(self):
        return Deck.objects.filter(owner=self.request.user)

class DeckDetailView(LoginRequiredMixin, DetailView):
    model=Deck
    context_object_name='deck'

    @override
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cards'] = Card.objects.filter(deck=self.get_object())
        return context

class DeckCreateView(LoginRequiredMixin, CreateView):
    model=Deck
    fields=['name']

    @override
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class CardDetailView(LoginRequiredMixin, DetailView):
    model=Card
    context_object_name='card'

class CardCreateView(LoginRequiredMixin, CreateView):
    model=Card
    fields=['front', 'back']

    @override
    def form_valid(self, form):
        form.instance.deck = Deck.objects.get(pk=self.kwargs.get('deck_pk'))
        return super().form_valid(form)

class CardUpdateView(LoginRequiredMixin, UpdateView):
    model=Card
    fields=['front', 'back']