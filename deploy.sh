docker-compose down
docker-compose up --build -d
docker-compose exec web_api python manage.py collectstatic --noinput
