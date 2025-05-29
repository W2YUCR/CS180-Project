from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponse
from django.views.generic import View, TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView

from quiz.models import Quiz
from decks.models import Card, Deck

from typing import override

def quiz_list_view(request):
    deck_list = Deck.objects.filter(owner=request.user)
    return render(request, "quiz/quiz_list.html", {"deck_list": deck_list})

# Create your views here.
class QuizView(TemplateView):
    template_name = "quiz/quiz.html"
    
    @override
    def get_context_data(self, **kwargs):
        pk = self.kwargs["pk"]
        quiz = Quiz.objects.get(pk=pk)
        deck = quiz.deck  # assuming quiz has a ForeignKey to Deck
        
        context = super().get_context_data(**kwargs)
        context["num_cards"] = quiz.cards.count()
        context["pk"] = pk
        context["deck"] = deck  # Add deck object to context
        return context


class QuizCurrentView(View):
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
    def post(self, request, *args, **kwargs):
        pk = self.kwargs["pk"]
        quiz = Quiz.objects.get(pk=pk)
        quiz.index += 1
        quiz.save()
        # Placeholder, we don't actually use the response for anything
        return JsonResponse({"success": 200})


class QuizCreateView(CreateView):
    model = Quiz
    fields = ["seconds_per_card"]

    @override
    def form_valid(self, form):
        deck = Deck.objects.get(pk=self.kwargs["deck_pk"])
        form.instance.deck = deck
        form.instance.index = 0
        quiz = form.save()
        for i, card in enumerate(Card.objects.filter(deck=deck)):
            quiz.cards.add(card, through_defaults={"index": i})
        return super().form_valid(form)

class QuizListView(ListView):
    model = Quiz
    template_name = "quiz/quiz_list.html"
    context_object_name = "quiz_list"

    @override
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Quiz.objects.filter(users=self.request.user)
        return Quiz.objects.none()

    
    
    
class QuizDetailView(DetailView):
    model = Quiz
    template_name = 'quiz/quiz_detail.html'  