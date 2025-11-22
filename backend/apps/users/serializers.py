from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'pseudo')
        read_only_fields = ('id',)

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            pseudo=validated_data.get('pseudo', '')
        )
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'pseudo')
        read_only_fields = ('id', 'username', 'email')

    def update(self, instance, validated_data):
        instance.pseudo = validated_data.get('pseudo', instance.pseudo)
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
        instance.save()
        return instance