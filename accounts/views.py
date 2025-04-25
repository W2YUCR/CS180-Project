from django.shortcuts import render, redirect
from django.views.generic import CreateView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from typing import override
from decks.models import Deck


# Create your views here.
class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "accounts/signup.html"


class UserProfileView(DetailView):
    model = User
    context_object_name = "user"
    template_name = "accounts/profile.html"

    @override
    def get_object(self):
        if "pk" in self.kwargs:
            return User.objects.get(pk=self.kwargs["pk"])
        elif self.request.user.is_authenticated:
            return self.request.user
        else:
            return redirect('accounts/login');

    @override
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["deck_list"] = self.object.deck_set.filter(published=True)
        return context
    