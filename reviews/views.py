from django.shortcuts import render
from django.views.generic import TemplateView
from decks.models import Deck
from typing import override


# Create your views here.
class ReviewView(TemplateView):
    template_name = "reviews/review.html"

    @override
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["deck_pk"] = self.kwargs["deck_pk"]
        return context
    