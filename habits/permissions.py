from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # Проверяем, является ли пользователь владельцем объекта.
        return obj.user == request.user


class IsOwnerOrPublic(permissions.BasePermission):

    # Проверяем, является ли пользователь владельцем объекта или привычка публичная.
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or obj.is_published
