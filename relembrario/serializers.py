from rest_framework import serializers
from relembrario.models import Lembrancas, Tag


class LembrancasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lembrancas
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'
