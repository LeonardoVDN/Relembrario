# serializers.py

from rest_framework import serializers
from relembrario.models import Lembrancas, Tag, Profile
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Profile
        fields = ['display_name', 'profile_picture']

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=False, allow_null=True)
    password = serializers.CharField(write_only=True, required=False, validators=[validate_password])
    new_password = serializers.CharField(write_only=True, required=False, validators=[validate_password])

    class Meta:
        model = User
        fields = ['username', 'email', 'profile', 'password', 'new_password']
        read_only_fields = ['username']

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', {})
        password = validated_data.pop('password', None)
        new_password = validated_data.pop('new_password', None)

        # Atualizar campos do usuário
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Atualizar senha se fornecida
        if password and new_password:
            if instance.check_password(password):
                instance.set_password(new_password)
            else:
                raise serializers.ValidationError({'password': 'Senha atual incorreta.'})

        instance.save()

        # Atualizar campos do perfil
        profile = getattr(instance, 'profile', None)
        if profile_data:
            if not profile:
                # Se o profile não existir, crie um novo
                profile = Profile.objects.create(user=instance)
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()

        return instance

class LembrancasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lembrancas
        fields = '__all__'
        read_only_fields = ['usuario']

    def create(self, validated_data):
        validated_data['usuario'] = self.context['request'].user
        return super().create(validated_data)

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'
        read_only_fields = ['usuario']

    def create(self, validated_data):
        validated_data['usuario'] = self.context['request'].user
        return super().create(validated_data)

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "As senhas não correspondem."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2', None)
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        # Opcional: criar perfil automaticamente
        Profile.objects.create(user=user)
        return user
