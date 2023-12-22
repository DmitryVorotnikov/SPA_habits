# SPA_habits (ENG)

## Project Description
This is a Single Page Application (SPA) inspired by the book "Atomic Habits" by James Clear. The project is designed to assist users in developing new beneficial habits and eliminating negative ones using the methodology outlined in the book.

## Project Idea
The main goal of the project is to help users create, implement, and track beneficial habits following the methodology presented in the book "Atomic Habits". Users have the ability to share their habits publicly so that others can also incorporate them into their lives.

## Project Functionalities
- The application provides a Full REST API using Django Rest Framework.
- Authentication is performed through JWT token mechanism.
- PostgresQL is used for data storage.
- Habit model (Habit) and user model (User).
- Custom data validation and pagination are implemented.
- Ability to share habits publicly for other users to use.
- Integration with the Telegram Bot API to deliver information to Telegram users.
- Asynchronous tasks via Celery and Celery-beat with Redis as a broker.
- CORS settings for security.
- Project settings and dependencies can be found in the `requirements.txt` file.
- Sample environment variables for quick local project setup are provided in the `.env.sample` file.
- Usage of Swagger and Redoc for API documentation following the OpenAPI standard.
- Includes flake8 report and test coverage report.



# SPA_habits (RUS)

## Описание проекта
Это веб-приложение SPA (Single Page Application), вдохновленно книгой "Атомные привычки" Джеймса Клира. Проект создан для помощи пользователям в разработке новых полезных привычек и избавлении от негативных через методику, описанную в книге.

## Идея проекта
Главная цель проекта - помочь пользователям создавать, внедрять и отслеживать полезные привычки согласно методике, представленной в книге "Атомные привычки". Пользователи имеют возможность делиться своими привычками публично, чтобы другие могли также внедрить их в свою жизнь.

## Функциональности проекта
- Приложение предоставляет Full REST API, используя Django Rest Framework.
- Авторизация осуществляется через механизм токенов JWT.
- Для хранения данных используется база данных PostgresQL.
- Модель привычки (Habit) и модель пользователя (User)
- Реализованны кастомная валидация данных, пагинация данных. 
- Возможность делиться привычками публично для использования другими пользователями.
- Интеграция с Telegram Bot API для вывода информации в Телеграм пользователям.
- Асинхронные задачи через Celery и Celery-beat с брокером Redis.
- Настройки CORS для обеспечения безопасности.
- Настройки и зависимости проекта можно найти в файле `requirements.txt`.
- Примеры переменных окружения для быстрого разворачивания проекта локально представлены в файле `.env.sample`.
- Использование Swagger и Redoc для документации API по стандарту OpenAPI.
- Присутствуют отчет flake8 и отчет покрытия тестами.
