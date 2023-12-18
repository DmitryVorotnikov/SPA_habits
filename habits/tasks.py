from datetime import timedelta, datetime, date

import requests
from celery import shared_task
from django.utils import timezone

from config.settings import TELEGRAM_URL, TELEGRAM_TOKEN
from habits.models import Habit


@shared_task
def task_send_tg_message():
    # Словарь для фильтра.
    filter_habits = {'is_pleasant_habit': False}

    habits = Habit.objects.filter(**filter_habits)
    for habit in habits:

        # Получение периодичности в количествах дней.
        if habit.periodicity == 'DAILY':
            interval = 1
        elif habit.periodicity == 'EVERY_TWO_DAYS':
            interval = 2
        elif habit.periodicity == 'EVERY_THREE_DAYS':
            interval = 3
        elif habit.periodicity == 'EVERY_FOUR_DAYS':
            interval = 4
        elif habit.periodicity == 'EVERY_FIFTH_DAY':
            interval = 5
        elif habit.periodicity == 'EVERY_SIXTH_DAY':
            interval = 6
        elif habit.periodicity == 'WEEKLY':
            interval = 7

        # Получение текущего даты-времени с учетом часового пояса и без информации о часовом поясе.
        current_datetime = timezone.localtime(timezone.now()).replace(tzinfo=None)  # datetime.datetime

        # Использование текущего дня для преобразования habit.started_at в объект datetime.datetime.
        today_date = date.today()
        habit_started_datetime = datetime.combine(today_date, habit.started_at)  # datetime.datetime

        if habit.last_message_time:
            # Получение даты-времени последнего сообщения с учетом часового пояса и без информации о часовом поясе.
            last_message_time = timezone.localtime(habit.last_message_time).replace(tzinfo=None)  # datetime.datetime

            # Вычисление даты-времени прошедшего с момента отправки последнего сообщение.
            time_passed = last_message_time - habit_started_datetime  # datetime.datetime

            if time_passed >= timedelta(days=interval):
                # Если дата-время прошедшее с момента последнего сообщения больше
                # периодичности, то отправляем сообщение.
                requests.post(
                    url=f'{TELEGRAM_URL}{TELEGRAM_TOKEN}/sendMessage',
                    data={
                        'chat_id': habit.user.chat_id,
                        'text': f'Настало время для полезной привычки: {habit.action}'
                    }
                )

                # Обновляем время последнего сообщение на текущее.
                habit.last_message_time = current_datetime
                habit.save()

        elif not habit.last_message_time:
            # Вычисление даты-времени от текущего момента до даты-времени начала привычки.
            time_passed = current_datetime - habit_started_datetime  # datetime.datetime

            if timedelta(seconds=1) <= time_passed <= timedelta(minutes=5):
                # Если дата-время от текущего момента до даты-времени начала привычки, в
                # пределах от 1 секунды до 5 минут, то отправляем первое сообщение.
                requests.post(
                    url=f'{TELEGRAM_URL}{TELEGRAM_TOKEN}/sendMessage',
                    data={
                        'chat_id': habit.user.chat_id,
                        'text': f'Настало время обзавестись полезной привычкой: {habit.action}'
                    }
                )

                # Обновляем время последнего сообщение на текущее.
                habit.last_message_time = current_datetime
                habit.save()
