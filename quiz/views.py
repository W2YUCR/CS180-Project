import random
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponse
from django.views.generic import View, TemplateView

from quiz.models import Quiz
from decks.models import Card, Deck

from typing import override

# Create your views here.
class QuizView(TemplateView):
    template_name = "quiz/quiz.html"

    @override
    def get_context_data(self, **kwargs):
        pk = self.kwargs["pk"]
        quiz = Quiz.objects.get(pk=pk)
        context = super().get_context_data(**kwargs)
        context["num_cards"] = quiz.cards.count()
        return context


class QuizCurrentView(View):
    @override
    def get(self, request, *args, **kwargs):
        pk = self.kwargs["pk"]
        quiz = Quiz.objects.get(pk=pk)
        if quiz.index < quiz.cards.count():
            card = quiz.cards.get(quizcard__index=quiz.index)
            return JsonResponse(
                {
                    "finished": False,
                    "front": card.front,
                    "back": card.back,
                    "index": quiz.index,
                }
            )
        else:
            return JsonResponse({"finished": True})


class QuizNextView(View):
    @override
    def post(self, request, *args, **kwargs):
        pk = self.kwargs["pk"]
        quiz = Quiz.objects.get(pk=pk)
        quiz.index += 1
        quiz.save()
        # Placeholder, we don't actually use the response for anything
        return JsonResponse({"success": 200})


class QuizCreateView(View):
    def post(self, request, *args, **kwargs):
        deck = Deck.objects.get(pk=request.POST.get("deck_pk"))
        quiz = Quiz.objects.create(deck=deck, index=0)
        cards = list(Card.objects.filter(deck = deck))
        random.shuffle(cards)
        for i, card in enumerate(cards):
            quiz.cards.add(card, through_defaults={"index": i})
        quiz.save()
        return redirect(reverse_lazy("quiz-view", kwargs={"pk": quiz.pk}))
