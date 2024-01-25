docker-compose down
docker-compose up --build -d
docker-compose exec web python manage.py collectstatic --noinput
