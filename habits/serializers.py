from rest_framework import serializers

from habits.models import Habit
from habits.validators import validator_habit


class HabitCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = (
            'id',
            'pleasant_habit',
            'location',
            'started_at',
            'action',
            'periodicity',
            'reward',
            'action_time_in_second',
            'is_pleasant_habit',
            'is_published',
        )
        read_only_fields = ('id',)

    def validate(self, data):
        validator_habit(
            pleasant_habit=data.get('pleasant_habit', None),
            started_at=data.get('started_at', None),
            periodicity=data.get('periodicity', None),
            reward=data.get('reward', None),
            is_pleasant_habit=data.get('is_pleasant_habit', None),
        )
        return data

    def create(self, validated_data):
        """ Метод укажет текущего пользователя как создателя привычки. """
        # Получаем текущего пользователя из контекста запроса.
        user = self.context['request'].user
        # Создаем привычку, указывая пользователя
        habit = Habit.objects.create(user=user, **validated_data)

        return habit


class HabitListRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'
