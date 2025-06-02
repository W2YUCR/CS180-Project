# decks/views.py
import random 
from django.http.request import HttpRequest
from django.urls import reverse_lazy
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import MultipleObjectMixin
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect
from decks.models import Card, Deck
from typing import override, Protocol

import requests


# This is probably not a good idea but it fixes the type errors...
# https://mypy.readthedocs.io/en/latest/more_types.html#mixin-classes
class ObjectViewProtocol[T](Protocol):
    request: HttpRequest

    def get_object(self) -> T: ...


class DeckListView(LoginRequiredMixin, ListView):
    context_object_name = "deck_list"

    @override
    def get_queryset(self):
        assert isinstance(self.request.user, User)
        return Deck.objects.filter(owner=self.request.user)


class RestrictedToDeckOwnerMixin(LoginRequiredMixin, PermissionRequiredMixin):
    @override
    def has_permission(self: ObjectViewProtocol[Deck]):
        return self.get_object().owner == self.request.user


class ShareableDeckMixin(LoginRequiredMixin, PermissionRequiredMixin):
    @override
    def has_permission(self: ObjectViewProtocol[Deck]):
        return (
            self.get_object().owner == self.request.user
            or self.get_object().published == True
        )


class DeckDetailView(ShareableDeckMixin, DetailView):
    model = Deck
    context_object_name = "deck"
    @override
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cards = list(Card.objects.filter(deck=self.get_object()))

        if self.request.GET.get("shuffle") == "true":
            random.shuffle(cards)

        context["cards"] = cards
        context["shuffled"] = self.request.GET.get("shuffle") == "true"
        return context



class DeckCreateView(LoginRequiredMixin, CreateView):
    model = Deck
    fields = ["name", "description"]

    @override
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class DeckUpdateView(RestrictedToDeckOwnerMixin, UpdateView):
    model = Deck
    fields = ["name", "description", "published"]


class DeckDeleteView(RestrictedToDeckOwnerMixin, DeleteView):
    model = Deck
    success_url = reverse_lazy("decks")

import requests


class SharedDecksView(ListView):
    context_object_name = "deck_list"
    template_name = "decks/shared.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_query = self.request.GET.get("search", "")
        context["search"] = search_query

        if search_query:
            try:
                api_url = "http://aloftballoon.pythonanywhere.com/api/value"
                params = {
                    "user_string": search_query,
                    "user_id": "",
                    "insertOrNot": 0
                }
                response = requests.get(api_url, params=params)
                response.raise_for_status()
                data = response.json()
                raw_strings = data.get("strings", [])
                context["api_results"] = [s.replace("_", "\n") for s in raw_strings]
            except Exception as e:
                context["api_results"] = {"error": str(e)}

        return context

    def get_queryset(self):
        return Deck.objects.select_related("owner").filter(**{"published": True})


class RestrictedToCardOwnerMixin(LoginRequiredMixin, PermissionRequiredMixin):
    @override
    def has_permission(self: ObjectViewProtocol[Card]):
        return self.get_object().deck.owner == self.request.user


class ShareableCardMixin(LoginRequiredMixin, PermissionRequiredMixin):
    @override
    def has_permission(self: ObjectViewProtocol[Card]):
        return (
            self.get_object().deck.owner == self.request.user
            or self.get_object().deck.published == True
        )


class CardDetailView(ShareableCardMixin, DetailView):
    model = Card
    context_object_name = "card"





class CardCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Card
    fields = ["front", "back"]

    @override
    def has_permission(self):
        return (
            Deck.objects.get(pk=self.kwargs.get("deck_pk")).owner == self.request.user
        )

    @override
    def form_valid(self, form):
        deck = Deck.objects.get(pk=self.kwargs.get("deck_pk"))
        form.instance.deck = deck

        front = form.cleaned_data.get("front", "").strip()
        back = form.cleaned_data.get("back", "").strip()
        user_string = f"Front: {front}_Back: {back}"

        try:
            api_url = "http://aloftballoon.pythonanywhere.com/api/value"
            params = {
                "user_string": user_string,
                "user_id": "",  
                "insertOrNot": 1
            }
            response = requests.get(api_url, params=params)
            response.raise_for_status()
            print("API success:", response.json())
        except Exception as e:
            print("API call failed:", e)

        return super().form_valid(form)




class CardUpdateView(RestrictedToCardOwnerMixin, UpdateView):
    model = Card
    fields = ["front", "back"]


class CardDeleteView(RestrictedToCardOwnerMixin, DeleteView):
    model = Card

    @override
    def get_success_url(self):
        return self.get_object().deck.get_absolute_url()

 