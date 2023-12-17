from rest_framework import serializers

from users.models import User


class UserCreateForAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserCreateSerializer(serializers.ModelSerializer):
    chat_id = serializers.CharField(min_length=6, required=True, allow_null=False)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'chat_id')


class UserListRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserUpdateForAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserUpdateSerializer(serializers.ModelSerializer):
    chat_id = serializers.CharField(min_length=6, required=True, allow_null=False)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'chat_id')
