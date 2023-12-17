from django.contrib import admin

from habits.models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'action',
        'action_time_in_minutes',
        'started_at',
        'location',
        'pleasant_habit',
        'reward',
        'periodicity',
        'is_pleasant_habit',
        'is_published',
    )
    list_filter = ('user', 'periodicity', 'is_pleasant_habit', 'is_published',)
    search_fields = ('user', 'action', 'location',)
