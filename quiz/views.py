from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponse
from django.views.generic import View, TemplateView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import get_object_or_404

from quiz.models import Quiz
from decks.models import Card, Deck
import logging

from typing import override

# Create a logger instance
logger = logging.getLogger('quiz')

# Create your views here.
class QuizView(TemplateView):
    template_name = "quiz/quiz.html"

    @override
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs["pk"]
        quiz = get_object_or_404(Quiz, pk=pk)
        cards = quiz.cards.all()
        first_card = cards.first()
        deck = first_card.deck if first_card else None
        context["quiz"] = quiz
        context["cards"] = cards
        context["num_cards"] = cards.count()
        context["deck"] = deck
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
        for i, card in enumerate(Card.objects.filter(deck=deck)):
            quiz.cards.add(card, through_defaults={"index": i})
        quiz.save()
        return redirect(reverse_lazy("quiz-view", kwargs={"pk": quiz.pk}))
    
class QuizPrevView(View):
    def post(self, request, *args, **kwargs):
        pk = self.kwargs["pk"]
        quiz = Quiz.objects.get(pk=pk)
        if quiz.index > 0:
            quiz.index -= 1
            quiz.save()
        return JsonResponse({"success": 200})