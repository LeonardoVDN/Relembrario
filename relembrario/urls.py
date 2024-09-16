from django.urls import path
from relembrario.views import initial_page

urlpatterns = [
    path('', initial_page)
]
