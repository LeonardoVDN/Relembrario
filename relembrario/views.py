from relembrario.models import Lembrancas, Tag
from relembrario.serializers import LembrancasSerializer, TagSerializer
from rest_framework import viewsets

class LembrancasViewSet(viewsets.ModelViewSet):
    queryset = Lembrancas.objects.all()
    serializer_class = LembrancasSerializer

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
