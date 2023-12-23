from rest_framework import serializers

from users.models import User
from users.services import password_hashing_on_creation, password_hashing_on_update


class UserCreateUpdateForAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        password_hashing_on_creation(validated_data)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        password_hashing_on_update(validated_data)
        return super().update(instance, validated_data)


class UserCreateUpdateSerializer(serializers.ModelSerializer):
    chat_id = serializers.CharField(min_length=6, required=True, allow_null=False)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'chat_id')

    def create(self, validated_data):
        password_hashing_on_creation(validated_data)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        password_hashing_on_update(validated_data)
        return super().update(instance, validated_data)


class UserListRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
