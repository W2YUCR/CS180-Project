from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request: HttpRequest) -> HttpResponse:
    return render(request, 'core/index.html')

def create(request: HttpRequest) -> HttpResponse:
    return render(request, 'core/create.html')