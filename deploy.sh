docker-compose down
docker-compose build
docker-compose up -d
docker-compose exec web_api python manage.py collectstatic
