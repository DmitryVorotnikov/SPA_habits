from django.contrib.auth.hashers import make_password
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

    def perform_create(self, serializer):
        """
        Hashes the user's password before saving it to the DB.
        Хеширует пароль пользователя перед записью в БД.
        """
        # Получение пароля из запроса.
        password = self.request.data.get('password')

        # Хеширование пароля.
        hashed_password = make_password(password)

        # Установка хешированного пароля в сериализатор перед сохранением в БД.
        serializer.save(password=hashed_password)

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

    def perform_update(self, serializer):
        """
        Hashes the user's password before saving it to the DB.
        Хеширует пароль пользователя перед записью в БД.
        """
        # Получение пароля из запроса.
        password = self.request.data.get('password')

        # Хеширование пароля, если он был изменен.
        if password:
            hashed_password = make_password(password)
            serializer.save(password=hashed_password)
        else:
            serializer.save()

    def get_queryset(self):
        if self.request.user.is_staff:
            # Администратор может редактировать всех пользователей.
            return User.objects.all()

        user_id = self.request.user.id
        return User.objects.filter(user=user_id).first()

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
