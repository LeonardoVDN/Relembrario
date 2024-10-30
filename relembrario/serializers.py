from rest_framework import serializers
from relembrario.models import Lembrancas, Tag
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['display_name', 'profile_picture']  # Inclua os campos necessários

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=False)  # Adicione o serializer de Profile

    class Meta:
        model = User
        fields = ['username', 'email', 'profile']

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', {})
        password = validated_data.pop('password', None)
        new_password = validated_data.pop('new_password', None)

        # Atualizar campos do usuário
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Alterar senha se fornecida
        if password and new_password:
            if instance.check_password(password):
                instance.set_password(new_password)
            else:
                raise serializers.ValidationError({'password': 'Senha atual incorreta.'})

        instance.save()

        # Atualizar campos do perfil
        profile = instance.profile
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

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "As senhas não correspondem."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user