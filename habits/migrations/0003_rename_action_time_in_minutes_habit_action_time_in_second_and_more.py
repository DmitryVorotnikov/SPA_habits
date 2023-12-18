# Generated by Django 4.2.8 on 2023-12-17 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('habits', '0002_habit_remove_usefulhabit_pleasant_habit_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='habit',
            old_name='action_time_in_minutes',
            new_name='action_time_in_second',
        ),
        migrations.AlterField(
            model_name='habit',
            name='periodicity',
            field=models.CharField(blank=True, choices=[('DAILY', 'Ежедневно'), ('EVERY_TWO_DAYS', 'Каждые два дня'), ('EVERY_THREE_DAYS', 'Каждые три дня'), ('EVERY_FOUR_DAYS', 'Каждые четыре дня'), ('EVERY_FIFTH_DAY', 'Каждый пятый день'), ('EVERY_SIXTH_DAY', 'Каждый шествой день'), ('WEEKLY', 'Еженедельно')], max_length=25, null=True, verbose_name='Периодичность'),
        ),
    ]