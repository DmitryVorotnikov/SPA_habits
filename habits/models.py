from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class UsefulHabit(models.Model):
    class PeriodicityType(models.TextChoices):
        # CHOICES для периодичности.
        DAILY = 'DAILY', 'Ежедневно'
        EVERY_TWO_DAYS = 'EVERY_TWO_DAYS', 'Каждые два дня'
        EVERY_THREE_DAYS = 'EVERY_THREE_DAYS', 'Каждые три дня'
        EVERY_FOUR_DAYS = 'EVERY_FOUR_DAYS', 'Каждые четыре дня'
        EVERY_FIFTH_DAY = 'EVERY_FIFTH_DAY', 'Каждый пятый день'
        EVERY_SIXTH_DAY = 'EVERY_SIXTH_DAY', 'Каждый шествой день'
        WEEKLY = 'WEEKLY', 'Еженедельно'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, verbose_name='Пользователь')
    pleasant_habit = models.ForeignKey(
        'PleasantHabit',
        on_delete=models.PROTECT,
        verbose_name='Приятная привычка',
        **NULLABLE
    )

    location = models.CharField(max_length=300, verbose_name='Место', **NULLABLE)
    started_at = models.TimeField(verbose_name='Начало в')
    action = models.TextField(max_length=1000, verbose_name='Действие')
    periodicity = models.CharField(
        max_length=25,
        choices=PeriodicityType.choices,
        default=PeriodicityType.DAILY,
        verbose_name='Периодичность'
    )
    reward = models.TextField(max_length=1000, verbose_name='Вознаграждение', **NULLABLE)
    action_time_in_minutes = models.PositiveSmallIntegerField(
        verbose_name='Длительность действия',
        validators=[MinValueValidator(1), MaxValueValidator(120)]
    )
    is_published = models.BooleanField(default=False, verbose_name='Признак публичности')

    def __str__(self):
        return f'Полезная привычка: {self.action}'

    class Meta:
        verbose_name = 'Полезная привычка'
        verbose_name_plural = 'Полезные привычки'
        ordering = ('user',)


class PleasantHabit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, verbose_name='Пользователь')

    location = models.CharField(max_length=300, verbose_name='Место', **NULLABLE)
    action = models.TextField(max_length=1000, verbose_name='Действие')
    action_time_in_minutes = models.PositiveSmallIntegerField(
        verbose_name='Длительность действия',
        validators=[MinValueValidator(1), MaxValueValidator(120)]
    )
    is_published = models.BooleanField(default=False, verbose_name='Признак публичности')

    def __str__(self):
        return f'Приятная привычка: {self.action}'

    class Meta:
        verbose_name = 'Приятная привычка'
        verbose_name_plural = 'Приятные привычки'
        ordering = ('user',)
