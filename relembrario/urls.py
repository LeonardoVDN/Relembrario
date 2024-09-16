from django.urls import path
from relembrario.views import estudantes

urlpatterns = [
    path('estudantes/',estudantes)
]
