from django.urls import reverse_lazy
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from decks.models import Deck
from typing import override

class DeckListView(LoginRequiredMixin, ListView):
    context_object_name='deck_list'
    @override
    def get_queryset(self):
        return Deck.objects.filter(owner=self.request.user)

class DeckDetailView(LoginRequiredMixin, DetailView):
    model=Deck
    context_object_name='deck'

class DeckCreateView(LoginRequiredMixin, CreateView):
    model=Deck
    fields=['name']

    @override
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)