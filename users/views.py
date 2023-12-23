from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from users.models import User
from users.paginators import UserPaginator
from users.serializers import UserCreateUpdateForAdminSerializer, UserCreateUpdateSerializer, UserListRetrieveSerializer


class UserCreateAPIView(generics.CreateAPIView):
    """
    View for creating a user. For both regular users and administrators.
    Представление для создания пользователя. Для пользователей и администраторов.
    """

    def get_serializer_class(self):
        if self.request.user.is_staff:
            # Администратор может заполнять любые поля.
            return UserCreateUpdateForAdminSerializer

        return UserCreateUpdateSerializer


class UserListAPIView(generics.ListAPIView):
    """
    View for viewing the list of users. For administrators only.
    Представление для просмотра списка пользователей. Только для администраторов.
    """
    permission_classes = [IsAdminUser]
    queryset = User.objects.all()
    serializer_class = UserListRetrieveSerializer
    pagination_class = UserPaginator

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ('id', 'first_name', 'last_name', 'email', 'chat_id',)
    search_fields = ('id', 'first_name', 'last_name', 'email', 'chat_id',)
    ordering_fields = ('is_active',)


class UserRetrieveAPIView(generics.RetrieveAPIView):
    """
    View for viewing a user. For administrators only.
    Представление для просмотра пользователя. Только для администраторов.
    """
    permission_classes = [IsAdminUser]
    queryset = User.objects.all()
    serializer_class = UserListRetrieveSerializer


class UserUpdateAPIView(generics.UpdateAPIView):
    """
    View for editing a user. For both regular users and administrators.
    Представление для редактирования пользователя. Для пользователей и администраторов.
    """
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(user=self.request.user).first()

        return queryset

    def get_serializer_class(self):
        if self.request.user.is_staff:
            # Администратор может редактировать все поля.
            return UserCreateUpdateForAdminSerializer

        return UserCreateUpdateSerializer


class UserDestroyAPIView(generics.DestroyAPIView):
    """
    View for deleting users. For administrators only.
    Представление для удаления пользователей. Только для администраторов.
    """
    permission_classes = [IsAdminUser]
    queryset = User.objects.all()
