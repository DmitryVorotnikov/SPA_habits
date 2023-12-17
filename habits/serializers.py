from rest_framework import serializers

from habits.models import Habit
from habits.validators import validator_habit


class HabitCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = (
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

        def validate(self, data):
            validator_habit(
                pleasant_habit=data['pleasant_habit'],
                location=data['location'],
                started_at=data['started_at'],
                periodicity=data['periodicity'],
                reward=data['reward'],
                is_pleasant_habit=data['is_pleasant_habit'],
            )
            return data


class HabitListRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'
