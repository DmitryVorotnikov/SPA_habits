docker-compose down
docker-compose up --build -d
docker-compose exec web_api python3 manage.py collectstatic --noinput
