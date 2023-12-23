from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated

from habits.models import Habit
from habits.paginators import HabitPaginator
from habits.permissions import IsOwnerOrReadOnly, IsOwnerOrPublic
from habits.serializers import HabitCreateUpdateSerializer, HabitListRetrieveSerializer


class HabitCreateAPIView(generics.CreateAPIView):
    """
    View for creating a habit.
    Представление для создания привычки.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = HabitCreateUpdateSerializer

    def perform_create(self, serializer):
        """ Метод укажет текущего пользователя как создателя курса. """
        serializer.save(user=self.request.user)


class HabitListAPIView(generics.ListAPIView):
    """
    View for viewing the list of habits for the current user.
    Представление для просмотра списка привычек текущего пользователя.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = HabitListRetrieveSerializer
    pagination_class = HabitPaginator

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = '__all__'
    search_fields = '__all__'
    ordering_fields = ('id',)

    def get_queryset(self):
        """ Метод вернет queryset с привычками текущего пользователя. """
        return Habit.objects.filter(user=self.request.user)


class HabitPublicListAPIView(generics.ListAPIView):
    """
    View for viewing the list of public habits.
    Представление для просмотра списка публичных привычек.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = HabitListRetrieveSerializer
    pagination_class = HabitPaginator
    queryset = Habit.objects.filter(is_published=True)

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = '__all__'
    search_fields = '__all__'
    ordering_fields = ('id',)


class HabitRetrieveAPIView(generics.RetrieveAPIView):
    """
    View for viewing a public habit or a habit of the current user.
    Представление для просмотра публичной привычки или привычки текущего пользователя.
    """
    permission_classes = [IsAuthenticated, IsOwnerOrPublic]
    serializer_class = HabitListRetrieveSerializer
    queryset = Habit.objects.all()


class HabitUpdateAPIView(generics.UpdateAPIView):
    """
    View for editing a habit of the current user.
    Представление для редактирования привычки текущего пользователя.
    """
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    serializer_class = HabitCreateUpdateSerializer
    queryset = Habit.objects.all()


class HabitDestroyAPIView(generics.DestroyAPIView):
    """
    View for deleting a habit of the current user.
    Представление для удаления привычки текущего пользователя.
    """
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    queryset = Habit.objects.all()
