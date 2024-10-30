from relembrario.models import Lembrancas, Tag
from relembrario.serializers import LembrancasSerializer, TagSerializer
from rest_framework import viewsets
from django.contrib.auth.models import User
from rest_framework import generics, permissions
from .serializers import RegisterSerializer, UserSerializer
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import PermissionDenied

class UserProfileView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

class LembrancasViewSet(viewsets.ModelViewSet):
    serializer_class = LembrancasSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Lembrancas.objects.filter(usuario=self.request.user)

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

    def get_object(self):
        obj = super().get_object()
        if obj.usuario != self.request.user:
            raise PermissionDenied("Você não tem permissão para acessar este objeto.")
        return obj

class TagViewSet(viewsets.ModelViewSet):
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Tag.objects.filter(usuario=self.request.user)

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

    def get_object(self):
        obj = super().get_object()
        if obj.usuario != self.request.user:
            raise PermissionDenied("Você não tem permissão para acessar este objeto.")
        return obj
    
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            if refresh_token is None:
                return Response({"detail": "O token de refresh é necessário."}, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"detail": "Logout realizado com sucesso."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"detail": "Erro ao fazer logout."}, status=status.HTTP_400_BAD_REQUEST)