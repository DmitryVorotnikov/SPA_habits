from django.contrib import admin

from habits.models import UsefulHabit, PleasantHabit


@admin.register(UsefulHabit)
class UsefulHabitAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'action',
        'action_time_in_minutes',
        'started_at',
        'location',
        'pleasant_habit',
        'reward',
        'periodicity',
        'is_published',
    )
    list_filter = ('user', 'periodicity', 'is_published',)
    search_fields = ('user', 'action', 'location',)


@admin.register(PleasantHabit)
class PleasantHabitAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'action',
        'action_time_in_minutes',
        'location',
        'is_published',
    )
    list_filter = ('user', 'is_published',)
    search_fields = ('user', 'action', 'location',)
