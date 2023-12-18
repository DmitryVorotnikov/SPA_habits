from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from habits.models import Habit
from users.models import User


class MyTestHelper:
    """
    Класс MyTestHelper содержит методы, которые упрощают работу с тестами и уменьшают объем кода.
    The MyTestHelper class contains methods that simplify working with tests and reduce code duplication.
    """

    @staticmethod
    def create_user():
        """
        Создает пользователя с заданными параметрами для использования в тестах.
        Creates a user with specified parameters for use in tests.
        """
        user = User.objects.create(
            email='user@test.com',
            password='test',
            is_active=True,
            is_staff=False,
            is_superuser=False
        )
        # Присвоение и хэширование пароля.
        # Password assignment and hashing.
        user.set_password('123456789')
        user.save()
        return user

    @staticmethod
    def create_auth_client(user):
        """
        Создает аутентифицированный клиент API для указанного пользователя.
        Creates an authenticated API client for the given user.
        """
        client = APIClient()
        client.force_authenticate(user=user)
        return client

    @staticmethod
    def create_new_obj_and_get_pk(client, url, data):
        """
        Создает новый объект и возвращает id (primary key) нового объекта.
        Creates a new object and returns the id (primary key) of the new object.
        """
        new_response = client.post(
            url,
            data=data
        )
        return new_response.data['id']


class HabitStatusCodeTestCase(APITestCase):
    """
    Тесты статуса кодов всех представлений HabitAPIView.
    """

    def setUp(self) -> None:
        # Создаем пользователя.
        self.user = MyTestHelper.create_user()
        # Проходим аутентификацию пользователем.
        self.client = MyTestHelper.create_auth_client(self.user)

        # Сохраняем данные для привычки.
        self.url_create = reverse('habits:habits_create')
        self.data = {
            'action': 'Habit test data',
            'action_time_in_second': 90,
            'is_pleasant_habit': True
        }

    def test_habit_create(self):
        """
        Тестирование статуса кода при создании привычки.
        """
        response = self.client.post(
            self.url_create,
            data=self.data
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_201_CREATED
        )

    def test_habit_list(self):
        """
        Тестирование статуса кода при просмотре списка привычек.
        """
        response = self.client.get(
            reverse('habits:habits_list'),
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_habit_public_list(self):
        """
        Тестирование статуса кода при просмотре списка публичных привычек.
        """
        response = self.client.get(
            reverse('habits:public_list'),
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_habit_retrieve(self):
        """
        Тестирование статуса кода при просмотре привычки.
        """
        habit_id = MyTestHelper.create_new_obj_and_get_pk(self.client, self.url_create, self.data)

        detail_url = reverse('habits:habits_get', kwargs={'pk': habit_id})
        response = self.client.get(detail_url)

        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_habit_update(self):
        """
        Тестирование статуса кода при обновлении привычки.
        """
        habit_id = MyTestHelper.create_new_obj_and_get_pk(self.client, self.url_create, self.data)

        detail_url = reverse('habits:habits_update', kwargs={'pk': habit_id})
        response = self.client.put(
            detail_url,
            data=self.data
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_habit_delete(self):
        """
        Тестирование статуса кода при удалении привычки.
        """
        habit_id = MyTestHelper.create_new_obj_and_get_pk(self.client, self.url_create, self.data)

        detail_url = reverse('habits:habits_delete', kwargs={'pk': habit_id})
        response = self.client.delete(detail_url)

        self.assertEquals(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )


class HabitListTestCase(APITestCase):
    """
    Тестирование данных при просмотре списка привычек.
    """

    def setUp(self) -> None:
        # Создаем пользователя.
        self.user = MyTestHelper.create_user()
        # Проходим аутентификацию пользователем.
        self.client = MyTestHelper.create_auth_client(self.user)

        # Сохраняем данные для привычки.
        self.url_habit_list = reverse('habits:habits_list')
        self.data = {
            'user': self.user,
            'action': 'Habit test data',
            'action_time_in_second': 90,
            'is_pleasant_habit': True
        }

        # Создаем привычку.
        self.habit = Habit.objects.create(
            user=self.data.get('user'),
            action=self.data.get('action'),
            action_time_in_second=self.data.get('action_time_in_second'),
            is_pleasant_habit=self.data.get('is_pleasant_habit')
        )

    def test_habit_list_data(self):
        """
        Тестирование данных при просмотре списка привычек.
        """
        response = self.client.get(
            self.url_habit_list,
        )
        self.assertEquals(
            response.json(),
            {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "id": self.habit.id,
                        "location": None,
                        "started_at": None,
                        "action": self.habit.action,
                        "periodicity": None,
                        "reward": None,
                        "action_time_in_second": self.habit.action_time_in_second,
                        "is_pleasant_habit": self.habit.is_pleasant_habit,
                        "is_published": False,
                        "last_message_time": None,
                        "user": self.habit.user.id,
                        "pleasant_habit": None
                    }
                ]
            }
        )


class HabitValidatorTestCase(APITestCase):
    """
    Тестирование валидатора для Habit.
    """

    def setUp(self) -> None:
        # Создаем пользователя.
        self.user = MyTestHelper.create_user()
        # Проходим аутентификацию польzзователем.
        self.client = MyTestHelper.create_auth_client(self.user)

        # Сохраняем данные для привычки.
        self.url_create = reverse('habits:habits_create')

    def test_habit_validator_reward(self):
        """
        Тестирование валидатора для Habit, с ошибкой валидации на выбор одного вида вознаграждения.
        """
        # Данные для создания привычки, с ошибкой валидации на выбор одного вида вознаграждения.
        self.data = {
            'started_at': '10:30',
            'action': 'action test data',
            'periodicity': 'EVERY_TWO_DAYS',
            'action_time_in_second': 90,
            'is_pleasant_habit': False
        }

        response = self.client.post(
            self.url_create,
            data=self.data
        )

        self.assertEqual(response.status_code, 400)

        error_message = response.json()['non_field_errors'][0]
        self.assertEqual(error_message, 'Должно быть указано вознаграждение или приятная привычка!')

    def test_habit_validator_started_at(self):
        """
        Тестирование валидатора для Habit, с ошибкой отсутствия старта привычки у полезной привычки.
        """
        # Данные для создания привычки, с ошибкой отсутствия старта привычки у полезной привычки.
        self.data = {
            'action': 'action test data',
            'periodicity': 'EVERY_TWO_DAYS',
            'action_time_in_second': 90,
            'reward': 'reward test data',
            'is_pleasant_habit': False
        }

        response = self.client.post(
            self.url_create,
            data=self.data
        )

        self.assertEqual(response.status_code, 400)

        error_message = response.json()['non_field_errors'][0]
        self.assertEqual(error_message, 'Должно быть указано время начала привычки!')

    def test_habit_validator_periodicity(self):
        """
        Тестирование валидатора для Habit, с ошибкой отсутствия периодичности у полезной привычки.
        """
        # Данные для создания привычки, с ошибкой отсутствия периодичности у полезной привычки.
        self.data = {
            'started_at': '10:30',
            'action': 'action test data',
            'action_time_in_second': 90,
            'reward': 'reward test data',
            'is_pleasant_habit': False
        }

        response = self.client.post(
            self.url_create,
            data=self.data
        )

        self.assertEqual(response.status_code, 400)

        error_message = response.json()['non_field_errors'][0]
        self.assertEqual(error_message, 'Должна быть указана периодичность привычки!')

    def test_habit_validator_pleasant_habit(self):
        """
        Тестирование валидатора для Habit, с ошибкой присутствия вознаграждения у полезной привычки.
        """
        # Данные для создания привычки, с ошибкой присутствия вознаграждения у полезной привычки.
        self.data = {
            'action': 'action test data',
            'action_time_in_second': 90,
            'reward': 'reward test data',
            'is_pleasant_habit': True
        }

        response = self.client.post(
            self.url_create,
            data=self.data
        )

        self.assertEqual(response.status_code, 400)

        error_message = response.json()['non_field_errors'][0]
        self.assertEqual(error_message, 'У приятной привычки не должно быть вознаграждения!')
