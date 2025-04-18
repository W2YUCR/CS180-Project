from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import View, TemplateView

from quiz.models import Quiz, QuizCard
from decks.models import Card, Deck


# Create your views here.
class QuizView(TemplateView):
    template_name = "quiz/quiz.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class QuizCreateView(View):
    def post(self, request, *args, **kwargs):
        deck = Deck.objects.get(pk=request.POST.get("deck_pk"))
        quiz = Quiz.objects.create(deck=deck)
        for i, card in enumerate(Card.objects.filter(deck=deck)):
            quiz.cards.add(card, through_defaults={"index": i})
        quiz.save()
        return redirect(reverse_lazy("quiz-view", kwargs={"pk": quiz.pk}))
