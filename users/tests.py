from django.core.management import call_command
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from habits.models import Habit
from users.models import User


class CustomCreateSuperUserTestCase(APITestCase):
    """
    Testing a Custom Create SuperUser command.
    """

    def test_create_superuser_successfully(self):
        """ Testing successful user creation. """
        call_command(
            'ccsu',
            '--email=admin@example.com',
            '--password=example_password',
            '--confirm_password=example_password',
            '--first_name=None',
            '--last_name=None',
            '--is_active=test',
            '--is_staff=test',
            '--is_superuser=test'
        )

        user_exists = User.objects.filter(email='admin@example.com').exists()
        self.assertTrue(user_exists)

    def test_exit_email_input(self):
        """ Testing 'exit' during email input. """
        call_command('ccsu', '--email=exit')

        user_exists = User.objects.filter(email='admin@example.com').exists()
        self.assertFalse(user_exists)

    def test_invalid_email(self):
        """ Testing invalid email input. """
        call_command('ccsu', '--email=invalid_email')

        user_exists = User.objects.filter(email='invalid_email').exists()
        self.assertFalse(user_exists)

    def test_exit_password_input(self):
        """ Testing 'exit' during password input. """
        call_command('ccsu', '--email=admin@example.com', '--password=exit')

        user_exists = User.objects.filter(email='admin@example.com').exists()
        self.assertFalse(user_exists)

    def test_invalid_password(self):
        """ Testing invalid password input. """
        call_command('ccsu', '--email=admin@example.com', '--password=123')

        user_exists = User.objects.filter(email='admin@example.com').exists()
        self.assertFalse(user_exists)

    def test_password_mismatch(self):
        """ Testing password mismatch input. """
        call_command('ccsu', '--email=admin@example.com', '--password=example_password',
                     '--confirm_password=mismatch_password')

        user_exists = User.objects.filter(email='admin@example.com').exists()
        self.assertFalse(user_exists)


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
            is_staff=True,
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


class UserStatusCodeTestCase(APITestCase):
    """
    Тесты статуса кодов всех представлений UserAPIView.
    """

    def setUp(self) -> None:
        # Создаем пользователя.
        self.user = MyTestHelper.create_user()
        # Проходим аутентификацию пользователем.
        self.client = MyTestHelper.create_auth_client(self.user)

        # Сохраняем данные для нового пользователя.
        self.url_create = reverse('users:users_create')
        self.data = {
            'email': 'testuser@gmail.com',
            'password': 'ksin532Vksdfk',
            'chat_id': 29347239487
        }

    def test_user_create(self):
        """
        Тестирование статуса кода при создании пользователя.
        """
        response = self.client.post(
            self.url_create,
            data=self.data
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_201_CREATED
        )

    def test_user_list(self):
        """
        Тестирование статуса кода при просмотре списка пользователей.
        """
        response = self.client.get(
            reverse('users:users_list'),
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_user_retrieve(self):
        """
        Тестирование статуса кода при просмотре одного пользователя.
        """
        user_id = MyTestHelper.create_new_obj_and_get_pk(self.client, self.url_create, self.data)

        detail_url = reverse('users:users_get', kwargs={'pk': user_id})
        response = self.client.get(detail_url)

        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_user_update(self):
        """
        Тестирование статуса кода при обновлении пользователя.
        """
        user_id = MyTestHelper.create_new_obj_and_get_pk(self.client, self.url_create, self.data)

        detail_url = reverse('users:users_update', kwargs={'pk': user_id})
        response = self.client.put(
            detail_url,
            data=self.data
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_user_delete(self):
        """
        Тестирование статуса кода при удалении пользователя.
        """
        user_id = MyTestHelper.create_new_obj_and_get_pk(self.client, self.url_create, self.data)

        detail_url = reverse('users:users_delete', kwargs={'pk': user_id})
        response = self.client.delete(detail_url)

        self.assertEquals(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )


class HabitListTestCase(APITestCase):
    """
    Тест просмотра списка привычек.
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

    def test_habit_list(self):
        """
        Тестирование данных при просмотре списка привычек.
        """
        response = self.client.get(
            self.url_habit_list,  # Или просто корень '/'
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
