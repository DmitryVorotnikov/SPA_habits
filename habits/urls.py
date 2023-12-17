from django.urls import path

from habits.apps import HabitsConfig
from habits.views import HabitCreateAPIView, HabitListAPIView, HabitPublicListAPIView, HabitRetrieveAPIView, \
    HabitUpdateAPIView, HabitDestroyAPIView

app_name = HabitsConfig.name

urlpatterns = [
    # URLs Habit:
    path('create/', HabitCreateAPIView.as_view(), name='habits_create'),
    path('', HabitListAPIView.as_view(), name='habits_list'),  # Список привычек текущего пользователя
    path('public', HabitPublicListAPIView.as_view(), name='public_list'),  # Список публичных привычек
    path('<int:pk>/', HabitRetrieveAPIView.as_view(), name='habits_get'),
    path('update/<int:pk>/', HabitUpdateAPIView.as_view(), name='habits_update'),
    path('delete/<int:pk>/', HabitDestroyAPIView.as_view(), name='habits_delete'),
]
