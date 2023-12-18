from rest_framework import serializers


def validator_habit(pleasant_habit, started_at, periodicity, reward, is_pleasant_habit):
    """
    Валидатор проверяет поля в соответствии с типом привычки.
    """
    if is_pleasant_habit:
        if pleasant_habit:
            raise serializers.ValidationError("У приятной привычки не должно быть связанной привычки!")
        elif started_at:
            raise serializers.ValidationError(
                "Приятная привычка начинается сразу после полезной, у нее не должно быть времени начал!")
        elif periodicity:
            raise serializers.ValidationError("У приятной привычки не должно быть периодичности!")
        elif reward:
            raise serializers.ValidationError("У приятной привычки не должно быть вознаграждения!")

    else:
        if bool(pleasant_habit) == bool(reward):
            raise serializers.ValidationError("Должно быть указано вознаграждение или приятная привычка!")
        elif pleasant_habit and not pleasant_habit.is_pleasant_habit:
            raise serializers.ValidationError("В связанные привычки могут попадать только приятные привычки!")
        elif not started_at:
            raise serializers.ValidationError("Должно быть указано время начала привычки!")
        elif not periodicity:
            raise serializers.ValidationError("Должна быть указана периодичность привычки!")
