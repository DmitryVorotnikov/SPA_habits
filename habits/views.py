from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated

from habits.models import Habit
from habits.paginators import HabitPaginator
from habits.serializers import HabitUsefulCreateUpdateSerializer, HabitPleasantCreateUpdateSerializer, \
    HabitListRetrieveSerializer


class HabitCreateAPIView(generics.CreateAPIView):
    """
    todo написать перевод
    Представление для создания привычки.
    """
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """ Метод вернет разные сериализаторы в зависимости от признака приятной привычки. """
        if self.request.data.get('is_pleasant_habit'):
            return HabitUsefulCreateUpdateSerializer
        return HabitPleasantCreateUpdateSerializer

    def perform_create(self, serializer):
        """ Метод укажет текущего пользователя как создателя курса. """
        serializer.save(user=self.request.user)


class HabitListAPIView(generics.ListAPIView):
    """
    todo написать перевод
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
    todo написать перевод
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
    permission_classes = [IsAuthenticated]
    serializer_class = HabitListRetrieveSerializer

    def get_queryset(self):
        """ Метод вернет queryset с публичными привычками или привычками текущего пользователя. """
        return Habit.objects.filter(Q(is_published=True) | Q(user=self.request.user))


class HabitUpdateAPIView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """ Метод вернет queryset с привычками текущего пользователя. """
        return Habit.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        """ Метод вернет разные сериализаторы в зависимости от признака приятной привычки. """
        if self.request.data.get('is_pleasant_habit'):
            return HabitUsefulCreateUpdateSerializer
        return HabitPleasantCreateUpdateSerializer


class HabitDestroyAPIView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """ Метод вернет queryset с привычками текущего пользователя. """
        return Habit.objects.filter(user=self.request.user)
