from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def initial_page(request):
    return render(request, 'relembrario/index.html')